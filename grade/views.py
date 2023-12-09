from collections import defaultdict

from bootstrap_modal_forms.generic import BSModalCreateView
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from classes.models import Stage
from grade.forms import StageTopicsStudentsForm, GradeModelForm, GradeModalModelForm, StageTestForm, StageForm, \
    DeleteGradeForm, StageStudentTestForm
from grade.models import Grade, MARK_CHOICES, TYPE_CHOICES
from topic.models import Topic, Skill


@staff_member_required
def add_grade(request):
    form = GradeModelForm(request.POST or None)
    if form.is_valid():
        saved_form = form.save(commit=False)
        if form.cleaned_data["grade_id"] is not None:
            grade = get_object_or_404(Grade, id=form.cleaned_data["grade_id"])
            edit_grade(grade, saved_form)
        else:
            saved_form.save()
        return JsonResponse({'grade_id': saved_form.pk, "success": True})
    return JsonResponse({'success': False})


def edit_grade(grade, saved_form):
    if saved_form.student is not None:
        grade.student = saved_form.student
    if saved_form.skill_level is not None:
        grade.skill_level = saved_form.skill_level
    grade.type = saved_form.type
    grade.value = saved_form.value
    if saved_form.comment is not None and saved_form.comment != "":
        grade.comment = saved_form.comment
    if saved_form.test is not None:
        grade.test = saved_form.test
    if saved_form.student_test is not None:
        grade.student_test = saved_form.student_test
    grade.save()


@staff_member_required
def delete_grade(request):
    form = DeleteGradeForm(request.POST or None)
    if form.is_valid() and form.cleaned_data["grade_id"] is not None:
        grade = get_object_or_404(Grade, id=form.cleaned_data["grade_id"])
        grade.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


# TODO: remove
class GradeCreateView(BSModalCreateView):
    template_name = 'create_grade.html'
    form_class = GradeModalModelForm
    success_message = 'Success: Book was created.'
    success_url = "/"


@staff_member_required
def choose_stage(request):
    user = request.user
    form = StageForm(user, request.POST or None)

    if form.is_valid():
        stage = form.cleaned_data["stage"]
        add_grade_type = form.cleaned_data["add_grade_type"]
        if add_grade_type == "test":
            return redirect(f"./stage/{stage.pk}/test")
        elif add_grade_type == "student_test":
            return redirect(f"./stage/{stage.pk}/student_test")
        elif add_grade_type == "topic_students":
            return redirect(f"./stage/{stage.pk}/topic")

    context = {"form": form}
    template_name = "choose_grade_stage.html"
    return render(request, template_name, context)


@staff_member_required
def choose_topic_students(request, pk):
    stage = get_object_or_404(Stage, pk=pk)
    form = StageTopicsStudentsForm(stage, request.POST or None)

    if form.is_valid():
        skills = form.cleaned_data["skills"]
        students = form.cleaned_data["students"]

        marks = sorted(MARK_CHOICES, key=lambda x: x[0]!=form.cleaned_data["default_mark"])
        types = sorted(TYPE_CHOICES, key=lambda x: x[0]!=form.cleaned_data["default_type"])
        return add_grades(request, stage, students, marks, types, "topic_students", skills=skills)

    context = {"form": form}
    template_name = "choose_topics_students.html"
    return render(request, template_name, context)


@staff_member_required
def choose_test(request, pk):
    stage = get_object_or_404(Stage, pk=pk)
    form = StageTestForm(stage, request.POST or None)

    if request.POST and form.is_valid():
        test = form.cleaned_data["test"]
        skills = test.skills.all()
        students = stage.students.all()
        marks = MARK_CHOICES
        types = TYPE_CHOICES
        return add_grades(request, stage, students, marks, types, "test", skills=skills, test=test)

    context = {"form": form}
    template_name = "choose_test.html"
    return render(request, template_name, context)


@staff_member_required
def choose_student_test(request, pk):
    stage = get_object_or_404(Stage, pk=pk)
    form = StageStudentTestForm(stage, request.POST or None)

    if request.POST and form.is_valid():
        student_test = form.cleaned_data["student_test"]
        skill_levels = student_test.skill_levels.all()
        students = stage.students.all()
        marks = MARK_CHOICES
        types = TYPE_CHOICES
        return add_grades(request, stage, students, marks, types, "student_test", skill_levels=skill_levels, student_test=student_test)

    context = {"form": form}
    template_name = "choose_student_test.html"
    return render(request, template_name, context)


@staff_member_required
def add_grades(request, stage, students, marks, types, grade_type, skills=None, skill_levels=None, test=None, student_test=None):
    if skills is None and skill_levels is None:
        return
    topic_to_skills_to_skill_levels = defaultdict(lambda: defaultdict(list))
    if skills is not None:
        for skill in skills:
            for level in skill.levels.all():
                topic_to_skills_to_skill_levels[skill.topic.title][(skill.title, skill.order)].append(level)
    if skill_levels is not None:
        for level in skill_levels:
            skill = Skill.objects.filter(levels__id=level.pk).first()
            topic_to_skills_to_skill_levels[skill.topic.title][(skill.title, skill.order)].append(level)
    topic_to_skills_to_skill_levels = {
        topic: {skill: levels for (skill, order), levels in sorted(skills.items(), key=lambda k: k[0][1])}
        for topic, skills in topic_to_skills_to_skill_levels.items()
    }
    if test is not None:
        grades = Grade.objects.filter(test_id=test.pk)
    elif student_test is not None:
        grades = Grade.objects.filter(student_test_id=student_test.pk)
    else:
        levels = [
            level for topic, skills in topic_to_skills_to_skill_levels.items()
            for skill, levels in skills.items() for level in levels
        ]
        grades = Grade.objects.filter(student_test__isnull=True).filter(test__isnull=True).filter(skill_level__in=levels)
    context = {
        "stage": stage, "topic_to_skills_to_skill_levels": topic_to_skills_to_skill_levels,
        "students": students, "marks": marks, "types": types, "grades": grades, "levels": [1, 2, 3],
        "grade_type": grade_type,
    }
    if test is not None:
        context["test"] = test
    if student_test is not None:
        context["student_test"] = student_test
    template_name = "add_grades.html"
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
