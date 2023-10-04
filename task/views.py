from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect, render

# Create your views here.
from topic.models import SkillLevel
from .forms import TaskModelForm, TaskGeneratorModelForm

from .models import Task, TaskGenerator
INITIAL_CODE = "def generator():\n    \n    return"


@staff_member_required
def add_task(request, pk_topic, pk_skill_level):
    form = TaskModelForm(request.POST or None)
    if form.is_valid():
        skill_level = get_object_or_404(SkillLevel, pk=pk_skill_level)
        task = form.save(commit=False)
        task.topic = skill_level.skills.all()[0].topic
        task.save()
        task_type = form.data["task_type"]
        if task_type in ["example", "both"]:
            skill_level.example_task = task
            skill_level.save()
        if task_type in ["task", "both"]:
            skill_level.tasks.add(task)
            skill_level.save()
        return redirect("../../../../")
    template_name = "task_form.html"
    context = {"form": form}
    return render(request, template_name, context)


@staff_member_required
def update_task(request, pk_topic, pk_task):
    task = get_object_or_404(Task, pk=pk_task)
    form = TaskModelForm(request.POST or None, instance=task)
    if form.is_valid():
        task_edit = form.save(commit=False)
        task_edit.save()
        return redirect(f"../../../")
    template_name = "form.html"
    context = {"form": form}
    return render(request, template_name, context)


@staff_member_required
def delete_task(request, pk_topic, pk_task):
    task = get_object_or_404(Task, pk=pk_task)
    if request.method == "POST":
        task.delete()
        return redirect("../../../")
    template_name = "delete_task.html"
    context = {"task": task}
    return render(request, template_name, context)


@staff_member_required
def add_task_generator(request, pk_topic, pk_skill_level):
    form = TaskGeneratorModelForm(request.POST or None, initial={"code": INITIAL_CODE})
    if form.is_valid():
        skill_level = get_object_or_404(SkillLevel, pk=pk_skill_level)
        task_generator = form.save(commit=False)
        task_generator.topic = skill_level.skills.all()[0].topic
        task_generator.save()
        skill_level.generators.add(task_generator)
        skill_level.save()
        return redirect("../../../../")
    template_name = "form.html"
    context = {"form": form}
    return render(request, template_name, context)


@staff_member_required
def update_task_generator(request, pk_topic, pk_generator):
    task_generator = get_object_or_404(TaskGenerator, pk=pk_generator)
    form = TaskGeneratorModelForm(request.POST or None, instance=task_generator)
    if form.is_valid():
        generator_edit = form.save(commit=False)
        generator_edit.save()
        return redirect(f"../../../")
    template_name = "form.html"
    context = {"form": form}
    return render(request, template_name, context)


@staff_member_required
def delete_task_generator(request, pk_topic, pk_generator):
    task_generator = get_object_or_404(TaskGenerator, pk=pk_generator)
    if request.method == "POST":
        task_generator.delete()
        return redirect("../../../")
    template_name = "delete_task_generator.html"
    context = {"task_generator": task_generator}
    return render(request, template_name, context)
