from collections import defaultdict

from bootstrap_modal_forms.generic import BSModalCreateView
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from classes.models import Stage
from grade.forms import StageTopicsStudentsForm, GradeModelForm, GradeModalModelForm
from grade.models import Grade, MARK_CHOICES, TYPE_CHOICES
from topic.models import Topic, Skill


# TODO: use one of below
@staff_member_required
def add_grade(request):
    form = GradeModelForm(request.POST or None)
    if form.is_valid():
        grade = form.save(commit=False)
        grade.save()
        return redirect("../")
    template_name = "form.html"
    context = {"form": form}
    return render(request, template_name, context)


class GradeCreateView(BSModalCreateView):
    template_name = 'create_grade.html'
    form_class = GradeModalModelForm
    success_message = 'Success: Book was created.'
    success_url = "/"


@staff_member_required
def choose_stage_topic_students(request):
    # stages = Stage.objects.filter(teacher=request.user)
    stage_chosen=False
    user = request.user
    form = StageTopicsStudentsForm(user, request.POST or None)

    if form.is_valid():
        stage = form.cleaned_data["stage"]
        if stage is not None:
            stage_chosen=True
        skills = form.cleaned_data["skills"]
        students = form.cleaned_data["students"]

        marks = sorted(MARK_CHOICES, key=lambda x: x[0]!=form.cleaned_data["default_mark"])
        types = sorted(TYPE_CHOICES, key=lambda x: x[0]!=form.cleaned_data["default_type"])
        # the second form with more fields available
        if len(skills) == 0 or len(students) == 0:
            form = StageTopicsStudentsForm(user, request.POST or None, stage=stage)
        else:
            topic_to_skills = defaultdict(list)
            for skill in skills:
                topic_to_skills[skill.topic.title].append(skill)
            context = {
                "stage": stage, "topic_to_skills": dict(topic_to_skills), "students": students,
                "levels": [1, 2, 3], "marks": marks, "types": types,
            }
            template_name = "add_grades.html"
            return render(request, template_name, context)

    context = {"stage_chosen": stage_chosen, "form": form}
    template_name = "choose_stage_topics_students.html"
    return render(request, template_name, context)


# TODO: refactor below
@staff_member_required
def skill_grade_edit(request, pk1, pk2):
    stages = Stage.objects.filter(teacher=request.user)
    topic = get_object_or_404(Topic, pk=pk1, stage__in=stages)
    skill = get_object_or_404(Skill, pk=pk2)
    context = {"topic": topic, "skill": skill, "title": "Edit grades"}
    template_name = "skill_grade_edit.html"

    if request.POST:
        level = request.POST["level"]
        return redirect(f"./{level}/")
    return render(request, template_name, context)


@staff_member_required
def skill_grade_edit_next(request, pk1, pk2, level):
    stages = Stage.objects.filter(teacher=request.user)
    topic = get_object_or_404(Topic, pk=pk1, stage__in=stages)
    skill = get_object_or_404(Skill, pk=pk2)
    context = {"topic": topic, "skill": skill, "level": "Chill", "title": "Edit grades"}
    if int(level) == 2:
        context["level"] = "Medium"
    if int(level) == 3:
        context["level"] = "Challenge"

    stage = topic.stage
    students = stage.students.all()
    add = {"stage": stage, "students": students}
    context = {**context, **add}

    last_grades = {}
    for student in students:
        grades = Grade.objects.filter(student=student, skill=skill, level=level)
        if len(grades) != 0:
            last_grades[student] = grades.last()
    context["last_grades"] = last_grades

    if len(last_grades) == 0:
        return render(
            request,
            "base.html",
            {
                "content": "Oh, there seems that there are no grades within this skill and level!",
            },
        )

    if request.POST:
        for key, val in request.POST.items():
            if key != "csrfmiddlewaretoken":
                student = get_object_or_404(User, pk=key)
                if val == "empty":
                    last_grades[student].delete()
                elif val != last_grades[student].value:
                    last_grades[student].value = val
                    last_grades[student].save()

        return redirect("../..")

    template_name = "skill_grade_edit_next.html"
    return render(request, template_name, context)


@staff_member_required
def skill_grade_delete(request, pk1, pk2):
    stages = Stage.objects.filter(teacher=request.user)
    topic = get_object_or_404(Topic, pk=pk1, stage__in=stages)
    skill = get_object_or_404(Skill, pk=pk2)
    context = {"topic": topic, "skill": skill, "title": "Delete grades"}
    template_name = "skill_grade_edit.html"

    if request.POST:
        level = request.POST["level"]
        return redirect(f"./{level}/")
    return render(request, template_name, context)


@staff_member_required
def skill_grade_delete_next(request, pk1, pk2, level):
    stages = Stage.objects.filter(teacher=request.user)
    topic = get_object_or_404(Topic, pk=pk1, stage__in=stages)
    skill = get_object_or_404(Skill, pk=pk2)
    context = {"topic": topic, "skill": skill, "level": "Chill"}
    if int(level) == 2:
        context["level"] = "Medium"
    if int(level) == 3:
        context["level"] = "Challenge"

    stage = topic.stage
    students = stage.students.all()
    add = {"stage": stage, "students": students}
    context = {**context, **add}

    last_grades = {}
    for student in students:
        grades = Grade.objects.filter(student=student, skill=skill, level=level)
        if len(grades) != 0:
            last_grades[student] = grades.last()
    context["last_grades"] = last_grades

    if len(last_grades) == 0:
        return render(
            request,
            "base.html",
            {
                "content": "Oh, there seems that there are no grades within this skill and level!",
            },
        )

    if request.POST:
        for grade in last_grades.values():
            grade.delete()
        return redirect("../..")

    template_name = "skill_grade_delete_next.html"
    return render(request, template_name, context)
