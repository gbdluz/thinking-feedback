from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect, render
from django.db import transaction

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
def topic_edit_whole_topic_view(request, pk):
    stages = Stage.objects.filter(teacher=request.user)
    topic = get_object_or_404(Topic, pk=pk, stage__in=stages)

    skill_objects = Skill.objects.filter(topic=topic).order_by("order")
    skills = []
    for skill in skill_objects:
        levels = [
            skill.levels.filter(level__startswith="1").all(),
            skill.levels.filter(level__startswith="2").all(),
            skill.levels.filter(level__startswith="3").all(),
        ]
        skills.append((skill, levels))
    template_name = "topic_edit_whole_topic.html"
    context = {"topic": topic, "skills": skills}
    context["empty"] = 0
    if len(skills) == 0:
        context["empty"] = 1
    return render(request, template_name, context)


@staff_member_required
def topic_student_view(request, pk):
    stages = Stage.objects.filter(teacher=request.user)
    topic = get_object_or_404(Topic, pk=pk, stage__in=stages)

    skill_objects = Skill.objects.filter(topic=topic).order_by("order")

    levels_count = {1: 1, 2: 1, 3: 1}
    levels = [1, 2, 3]
    for skill in skill_objects:
        for level in levels:
            count = skill.levels.filter(level__startswith=str(level)).count()
            if count > levels_count[level]:
                levels_count[level] = count

    table = {}
    for skill in skill_objects:
        table_row = {i: None for i in range(sum(levels_count.values()))}
        table[skill.order] = table_row

    for skill in skill_objects:
        id_init = 0
        for level in levels:
            lvls = [{"lvl": lvl, "included": False} for lvl in (skill.levels.filter(level__startswith=str(level)).all())]
            for lvl in lvls:
                if min([s.order for s in lvl["lvl"].skills.all()]) != skill.order:
                    for skill_inside in lvl["lvl"].skills.all():
                        for id in range(levels_count[level]):
                            if type(table[skill_inside.order][id_init+id])==dict and table[skill_inside.order][id_init+id]["lvl"].pk == lvl["lvl"].pk:
                                lvl["included"] = True
                                table[skill.order][id_init + id] = "rowspan"

            for lvl in lvls:
                if min([s.order for s in lvl["lvl"].skills.all()]) == skill.order:
                    saved = False
                    for id in range(levels_count[level]):
                        if table[skill.order][id_init + id] is None and not saved:
                            required_passes = False
                            for skill_inside in lvl["lvl"].skills.all():
                                if skill_inside.required_passes != lvl["lvl"].required_passes:
                                    required_passes = lvl["lvl"].required_passes
                            table[skill.order][id_init + id] = {"lvl": lvl["lvl"], "rowspan": lvl["lvl"].skills.count(), "required_passes": required_passes}
                            saved = True
                    if not saved:
                        print("Not saved - check what happened!")
            id_init += levels_count[level]

    skills = []
    rows = sorted(table.keys())
    for row, skill in zip(rows, skill_objects):
        cols = [table[row][i] for i in range(sum(levels_count.values()))]
        skills.append((skill, cols))

    template_name = "topic_student_view.html"
    width_multiplier = 250
    header = [
        ("Podstawowa", levels_count[1], levels_count[1]*width_multiplier),
        ("Średniozaawansowana", levels_count[2], levels_count[2]*width_multiplier),
        ("Zaawansowana", levels_count[3], levels_count[3]*width_multiplier),
    ]

    context = {"topic": topic, "skills": skills, "header": header, "table_width": sum([h[2] for h in header]) + 200}
    context["empty"] = 0
    if len(skills) == 0:
        context["empty"] = 1

    return render(request, template_name, context)


@staff_member_required
def add_topic(request, pk_stage):
    user = request.user
    form = TopicModelForm(user, request.POST or None, initial={"stage": pk_stage})
    if form.is_valid():
        topic = form.save(commit=False)
        topic.teacher = request.user
        topic.save()
        return redirect("../../..")
    template_name = "form.html"
    context = {"form": form}
    print("return")
    return render(request, template_name, context)


@staff_member_required
def add_skill(request, pk):
    stages = Stage.objects.filter(teacher=request.user)
    form = SkillModelForm(request.POST or None)
    if form.is_valid():
        skill = form.save(commit=False)
        topic = get_object_or_404(Topic, pk=pk, stage__in=stages)
        skill.topic = topic
        topic_skill_last = Skill.objects.filter(topic_id=pk).order_by("order").last()
        order = 1
        if topic_skill_last is not None:
            order = topic_skill_last.order + 1
        skill.order = order
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
def change_skill_order(request, pk, pk_skill, up_down):
    if up_down not in ["up", "down"]:
       raise ValueError(f"up_down {up_down} should be one of 'up', 'down'")
    skill = get_object_or_404(Skill, pk=pk_skill)
    other_skill_order = skill.order - 1 if up_down=="up" else skill.order + 1
    other_skills = Skill.objects.filter(topic_id=skill.topic.pk, order=other_skill_order).all()
    if len(other_skills) > 1:
        raise Exception("Too many skills with same order.")
    elif len(other_skills) == 0:
        print("Can't do it.")
    else:
        other_skill = other_skills.first()
        skill.order, other_skill.order = other_skill.order, skill.order
        with transaction.atomic():
            skill.save()
            other_skill.save()
    return redirect("../../../..")


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
