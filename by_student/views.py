from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from classes.models import Stage
from topic.models import Topic, Skill, Grade

# Create your views here.
@staff_member_required
def by_student(request):
    stages = Stage.objects.filter(teacher=request.user)
    students = {}
    for stage in stages:
        students[stage] = stage.students.all()
    context = {"students": students, "empty": 0}
    if len(stages) == 0:
        context["empty"] = 1
    template_name = "by_student.html"
    return render(request, template_name, context)


@staff_member_required
def by_student_pick_topic(request, pk):
    student = User.objects.get(pk=pk)
    stage = student.classes.all()[0]  #TODO: allow multiple user
    if stage.teacher != request.user:
        return redirect("/")
    qs = Topic.objects.filter(stage=stage)
    context = {"topic_list": qs, "student": student, "stage": stage}
    template_name = "by_student_pick_topic.html"
    return render(request, template_name, context)


@staff_member_required
def by_student_view(request, pk1, pk2):
    student = User.objects.get(pk=pk1)
    stage = student.classes.all()[0]
    if stage.teacher != request.user:
        return redirect("/")
    obj = get_object_or_404(Topic, pk=pk2)
    skill_list = Skill.objects.filter(topic=obj)
    context = {
        "skill_list": skill_list,
        "student": student,
        "topic": obj.title,
    }
    grades = {}
    student = User.objects.get(pk=pk1)
    for skill in skill_list:
        grades[skill] = {}
        for level in (1, 2, 3):
            grades[skill][level] = []
            temp = Grade.objects.filter(student=student, skill=skill, level=level)
            for grade in temp:
                grades[skill][level].append(grade)
    context["grades"] = grades
    template_name = "by_student_view.html"
    return render(request, template_name, context)


@staff_member_required
def by_student_update(request, pk1, pk2):
    obj = get_object_or_404(Topic, pk=pk2)
    student = User.objects.get(pk=pk1)
    stage = student.classes.all()[0]
    if stage.teacher != request.user:
        return redirect("/")
    skill_list = Skill.objects.filter(topic=obj)
    context = {"student": student, "skill_list": skill_list, "topic": obj.title}
    template_name = "by_student_update.html"
    if request.POST:
        for key, value in request.POST.items():
            if key != "csrfmiddlewaretoken" and value != "empty":
                skill_pk = key[:-1]
                skill = Skill.objects.get(topic=obj, pk=skill_pk)
                level = key[-1]
                grade = Grade(student=student, skill=skill, value=value, level=level)
                grade.save()
        return redirect("..")
    return render(request, template_name, context)


@staff_member_required
def by_student_edit(request, pk1, pk2):
    student = User.objects.get(pk=pk1)
    stage = student.classes.all()[0]
    if stage.teacher != request.user:
        return redirect("/")
    obj = get_object_or_404(Topic, pk=pk2)
    skill_list = Skill.objects.filter(topic=obj)
    context = {
        "skill_list": skill_list,
        "student": student,
        "topic": obj.title,
    }  #'slug': slug,
    grades = {}
    student = User.objects.get(pk=pk1)
    for skill in skill_list:
        grades[skill] = {}
        for level in (1, 2, 3):
            temp_grades = []
            temp = Grade.objects.filter(student=student, skill=skill, level=level)
            for grade in temp:
                temp_grades.append(grade)
            if len(temp_grades) > 1:
                grades[skill][level] = (temp_grades[:-1], temp_grades[-1])
            elif len(temp_grades) == 1:
                grades[skill][level] = ([], temp_grades[0])
            else:
                grades[skill][level] = ([], "")

    context["grades"] = grades
    template_name = "by_student_edit.html"

    if request.POST:
        for key, value in request.POST.items():
            if key != "csrfmiddlewaretoken":
                skill_pk = key[:-1]
                skill = Skill.objects.get(topic=obj, pk=skill_pk)
                level = key[-1]
                grade = Grade.objects.filter(
                    student=student, skill=skill, level=level,
                ).last()
                if value == "empty":
                    grade.delete()
                elif grade.value != value:
                    grade.value = value
                    grade.save()
        return redirect("..")

    return render(request, template_name, context)
