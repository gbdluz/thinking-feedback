from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect, render

# Create your views here.
from topic.models import Skill, Topic, SkillLevel
from classes.models import Stage

from .forms import (
    SkillModelForm, TopicModelForm, SkillLevelModelForm, SkillLevelNewSkillModelForm,
)


context = {}


@staff_member_required
def stage_all_topics(request):
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

    template_name = "stage_all_topics.html"
    return render(request, template_name, context)


@staff_member_required
def topic_detail_view(request, pk):
    stages = Stage.objects.filter(teacher=request.user)
    topic = get_object_or_404(Topic, pk=pk, stage__in=stages)

    skill_objects = Skill.objects.filter(topic=topic)
    skills = []
    for skill in skill_objects:
        levels = [
            skill.levels.filter(level__startswith="1").all(),
            skill.levels.filter(level__startswith="2").all(),
            skill.levels.filter(level__startswith="3").all(),
        ]
        skills.append((skill, levels))
    template_name = "topic_detail.html"
    context = {"topic": topic, "skills": skills}
    context["empty"] = 0
    if len(skills) == 0:
        context["empty"] = 1
    return render(request, template_name, context)


@staff_member_required
def add_topic(request):
    user = request.user
    form = TopicModelForm(user, request.POST or None)
    if form.is_valid():
        topic = form.save(commit=False)
        topic.teacher = request.user
        topic.save()
        return redirect("/topic")
    template_name = "form.html"
    context = {"form": form}
    return render(request, template_name, context)


@staff_member_required
def add_skill(request, pk):
    stages = Stage.objects.filter(teacher=request.user)
    form = SkillModelForm(request.POST or None)
    if form.is_valid():
        skill = form.save(commit=False)
        topic = get_object_or_404(Topic, pk=pk, stage__in=stages)
        skill.topic = topic
        skill.save()
        return redirect("..")
    template_name = "form.html"
    context = {"form": form}
    return render(request, template_name, context)


@staff_member_required
def add_skill_level(request, pk1, pk2):
    form = SkillLevelModelForm(request.POST or None)
    if form.is_valid():
        skill_level = form.save(commit=False)
        skill = get_object_or_404(Skill, pk=pk2)
        skill_level.save()
        skill_level.skills.add(skill)
        skill_level.save()
        return redirect("../../..")
    template_name = "form.html"
    context = {"form": form}
    return render(request, template_name, context)


@staff_member_required
def add_skill_to_skill_level(request, pk1, pk3):
    topic = get_object_or_404(Topic, pk=pk1)
    skill_level = get_object_or_404(SkillLevel, pk=pk3)
    form = SkillLevelNewSkillModelForm(topic, request.POST or None, instance=skill_level)
    if form.is_valid():
        skill_level = get_object_or_404(SkillLevel, pk=pk3)
        for skill in form.cleaned_data["skills"]:
            skill_level.skills.add(skill)
        skill_level.save()
        return redirect("../../..")
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
def update_skill(request, pk1, pk2):
    stages = Stage.objects.filter(teacher=request.user)
    topic = get_object_or_404(Topic, pk=pk1, stage__in=stages)
    skill = get_object_or_404(Skill, pk=pk2)
    form = SkillModelForm(request.POST or None, instance=skill)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.topic = topic
        obj.save()
        return redirect(f"../../../")
    template_name = "form.html"
    context = {"form": form}
    return render(request, template_name, context)


@staff_member_required
def delete_skill(request, pk1, pk2):
    stages = Stage.objects.filter(teacher=request.user)
    topic = get_object_or_404(Topic, pk=pk1, stage__in=stages)
    skill = get_object_or_404(Skill, pk=pk2)
    if request.method == "POST":
        skill.delete()
        return redirect("../../../")
    template_name = "delete_skill.html"
    context = {"skill": skill}
    return render(request, template_name, context)


@staff_member_required
def update_skill_level(request, pk1, pk3):
    skill_level = get_object_or_404(SkillLevel, pk=pk3)
    form = SkillLevelModelForm(request.POST or None, instance=skill_level)
    if form.is_valid():
        skill_level_edit = form.save(commit=False)
        # skill_level_edit.skills = skill_level.skills
        skill_level_edit.save()
        return redirect(f"../../../")
    template_name = "form.html"
    context = {"form": form}
    return render(request, template_name, context)


@staff_member_required
def delete_skill_level(request, pk1, pk3):
    skill_level = get_object_or_404(SkillLevel, pk=pk3)
    if request.method == "POST":
        skill_level.delete()
        return redirect("../../../")
    template_name = "delete_skill.html"
    context = {"skill_level": skill_level}
    return render(request, template_name, context)
