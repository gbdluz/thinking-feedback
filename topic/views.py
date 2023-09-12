from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

# Create your views here.
from topic.models import Grade, Skill, Topic
from classes.models import Stage

from .forms import (
    SkillModelForm, TopicModelForm,
)

# from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, PasswordResetForm


context = {}


@staff_member_required
def by_subject(request):
    stages = Stage.objects.filter(teacher=request.user)
    context["stages"] = stages

    topics = {}
    for stage in stages:
        temp = Topic.objects.filter(stage=stage)
        topics[stage] = temp
    context["topics"] = topics
    context["empty"] = 0
    if len(stages) == 0:
        context["empty"] = 1

    template_name = "by_subject.html"
    return render(request, template_name, context)


@staff_member_required
def topic_detail_view(request, pk):
    stages = Stage.objects.filter(teacher=request.user)
    obj = get_object_or_404(Topic, pk=pk, stage__in=stages)

    qs2 = Skill.objects.filter(topic=obj)
    template_name = "topic_detail.html"
    context = {"object": obj, "skill_list": qs2}
    context["empty"] = 0
    if len(qs2) == 0:
        context["empty"] = 1
    return render(request, template_name, context)


@staff_member_required
def add_topic(request):
    user = request.user
    form = TopicModelForm(user, request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.teacher = request.user
        obj.save()
        user = request.user
        form = TopicModelForm(user)
        return redirect("/topic")
    template_name = "form.html"
    context = {"form": form}
    return render(request, template_name, context)


@staff_member_required
def add_skill(request, pk):
    stages = Stage.objects.filter(teacher=request.user)
    form = SkillModelForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        topic = get_object_or_404(Topic, pk=pk, stage__in=stages)
        obj.topic = topic
        obj.save()
        return redirect("..")
    template_name = "form.html"
    context = {"form": form}
    return render(request, template_name, context)


@staff_member_required
def update_topic(request, pk):
    user = request.user
    stages = Stage.objects.filter(teacher=request.user)
    topic = get_object_or_404(Topic, pk=pk, stage__in=stages)
    form = TopicModelForm(user, request.POST or None, instance=topic)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.teacher = request.user
        obj.save()
        user = request.user
        form = TopicModelForm(user)
        return redirect("..")
    template_name = "form.html"
    context = {"form": form}
    return render(request, template_name, context)


@staff_member_required
def delete_topic(request, pk):
    stages = Stage.objects.filter(teacher=request.user)
    topic = get_object_or_404(Topic, pk=pk, stage__in=stages)
    if request.method == "POST":
        topic.delete()
        return redirect("../..")
    template_name = "delete_topic.html"
    context = {"topic": topic}
    return render(request, template_name, context)


@staff_member_required
def skill_update(request, pk1, pk2):
    stages = Stage.objects.filter(teacher=request.user)
    topic = get_object_or_404(Topic, pk=pk1, stage__in=stages)
    skill = get_object_or_404(Skill, pk=pk2)
    stage = topic.stage
    template_name = "skill_update.html"
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


@staff_member_required
def skill_edit(request, pk1, pk2):
    stages = Stage.objects.filter(teacher=request.user)
    topic = get_object_or_404(Topic, pk=pk1, stage__in=stages)
    skill = get_object_or_404(Skill, pk=pk2)
    form = SkillModelForm(request.POST or None, instance=skill)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.topic = topic
        obj.save()
        return redirect(f"../../{obj.pk}")
    template_name = "form.html"
    context = {"form": form}
    return render(request, template_name, context)


@staff_member_required
def skill_delete(request, pk1, pk2):
    stages = Stage.objects.filter(teacher=request.user)
    topic = get_object_or_404(Topic, pk=pk1, stage__in=stages)
    skill = get_object_or_404(Skill, pk=pk2)
    if request.method == "POST":
        skill.delete()
        return redirect("../../..")
    template_name = "delete_skill.html"
    context = {"skill": skill}
    return render(request, template_name, context)
