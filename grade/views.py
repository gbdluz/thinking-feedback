from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from classes.models import Stage
from grade.models import Grade
from topic.models import Topic, Skill


@staff_member_required
def grade_add(request, pk1, pk2):
    stages = Stage.objects.filter(teacher=request.user)
    topic = get_object_or_404(Topic, pk=pk1, stage__in=stages)
    skill = get_object_or_404(Skill, pk=pk2)
    stage = topic.stage
    template_name = "grade_add.html"
    students = stage.students.all()
    context = {"topic": topic, "skill": skill, "stage": stage, "students": students}

    if request.POST:
        for key in request.POST.keys():
            if key != "csrfmiddlewaretoken" and key != "level":
                student = User.objects.get(pk=key)
                value = request.POST[key]
                level = request.POST["level"]
                grade = Grade(student=student, skill=skill, value=value, level=level)
                grade.save()
        return redirect("../..")
    return render(request, template_name, context)


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
