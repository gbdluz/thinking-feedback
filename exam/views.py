from collections import defaultdict
from typing import List

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404

from exam.forms import StageForm, TestForm, StudentTestForm
from exam.generator import LatexCreator
from exam.models import Test, StudentTest, ChoiceTestTask, TestTask
from task.models import TaskGenerator
from topic.models import Skill, SkillLevel


@staff_member_required
def choose_stage(request):
    form = StageForm(request.POST or None)

    if form.is_valid():
        stage = form.cleaned_data["stage"]

        tests = Test.objects.filter(stage__teacher=request.user)
        student_tests = StudentTest.objects.filter(stage__teacher=request.user)
        students = User.objects.filter(classes__teacher=request.user)
        skills = Skill.objects.filter(topic__stage=stage)

        topic_to_skills = defaultdict(list)
        for skill in skills:
            topic_to_skills[skill.topic.title].append(skill)
        test_form = TestForm(stage, request.POST or None)
        student_test_form = StudentTestForm(stage, request.POST or None)
        context = {
            "tests": tests, "student_tests": student_tests, "stage": stage,
            "test_form": test_form, "student_test_form": student_test_form,
            "topic_to_skills": dict(topic_to_skills), "students": students,
        }
        template_name = "edit_tests.html"
        return render(request, template_name, context)

    context = {"form": form}
    template_name = "choose_stage.html"
    return render(request, template_name, context)


@staff_member_required
def create_test(request):
    form = TestForm(None, request.POST or None)
    if form.is_valid():
        test = form.save(commit=False)
        test.save()
        skills = form.cleaned_data["skills"]
        for skill in skills:
            test.skills.add(skill)
        return redirect("../")
    template_name = "form.html"
    context = {"form": form}
    return render(request, template_name, context)


@staff_member_required
def manage_test(request, pk: int):
    if request.POST:
        data = defaultdict(lambda: defaultdict(lambda: {}))
        for key, value in request.POST.items():
            keys = key.split("_")
            if len(keys) == 3:
                data[keys[0]][keys[1]][keys[2]] = value
        test = get_object_or_404(Test, pk=int(request.POST["test-id"]))
        test_data = data["test"]["0"]
        if test.name != test_data["name"]:
            test.name = test_data["name"]
            test.save()
        if test.groups != test_data["groups"]:
            test.groups = test_data["groups"]
            test.save()
        if test.date != test_data["date"]:
            test.date = test_data["date"]
            test.save()
        for choice_task_name, choice_task_data in data["choice-task"].items():
            if choice_task_data['page'] != '':
                if choice_task_name.startswith('skill'):
                    skill_id = int(choice_task_name.split('-')[1])
                    skill = get_object_or_404(Skill, pk=skill_id)
                    choice_test_task = ChoiceTestTask(test=test, skill=skill, page=choice_task_data['page'])
                    choice_test_task.save()
                else:
                    choice_test_task = get_object_or_404(ChoiceTestTask, pk=int(choice_task_name))
                    if choice_test_task.page != int(choice_task_data['page']):
                        choice_test_task.page = int(choice_task_data['page'])
                        choice_test_task.save()
        for task_name, task_data in data["task"].items():
            skill_id = int(task_data["skill-id"])
            choice_test_task = ChoiceTestTask.objects.filter(test_id=test.id, skill_id=skill_id).first()
            if choice_test_task:
                if task_name.startswith('skilllevel'):
                    generator_ids = [value for key, value in task_data.items() if key.startswith("generator")]
                    if len(generator_ids) > 0:
                        skill_level_id = int(task_name.split('-')[1])
                        skill_level = get_object_or_404(SkillLevel, pk=skill_level_id)
                        generate_all = True if task_data["all"]=="all" else False
                        test_task = TestTask(skill_level=skill_level, choice_test_task=choice_test_task, generate_all=generate_all)
                        test_task.save()
                        for generator_id in generator_ids:
                            generator = get_object_or_404(TaskGenerator, id=int(generator_id))
                            test_task.generators.add(generator)
                else:
                    test_task = get_object_or_404(TestTask, pk=int(task_name))
                    generate_all = True if task_data["all"]=="all" else False
                    if test_task.generate_all != generate_all:
                        test_task.generate_all = generate_all
                        test_task.save()
                    generator_ids = []
                    for key, value in task_data.items():
                        if key.startswith("generator"):
                            generator_ids.append(int(value))
                    for generator in test_task.generators.all():
                        if generator.pk not in generator_ids:
                            test_task.generators.remove(generator)
                    for id in generator_ids:
                        if not test_task.generators.filter(id=id).first():
                            generator = get_object_or_404(TaskGenerator, id=id)
                            test_task.generators.add(generator)
        return redirect(f".", request)

    test = Test.objects.filter(pk=pk).first()
    stage = test.stage
    skills = test.skills.all().order_by("pk")

    skills_data = []
    for skill in skills:
        choice_task = ChoiceTestTask.objects.filter(skill_id=skill.pk, test_id=pk).first()
        skill_levels: List[SkillLevel] = skill.levels.all().order_by("level")
        skill_levels_data = []
        for skill_level in skill_levels:
            task = None
            if choice_task is not None:
                task = TestTask.objects.filter(skill_level_id=skill_level.pk, choice_test_task_id=choice_task.pk).first()
            generators = skill_level.generators.all()
            generators_data = []
            for generator in generators:
                generator_data = {"generator": generator}
                if task is not None:
                    if task.generators.filter(id=generator.pk).first():
                        generator_data["checked"] = True
                generators_data.append(generator_data)
            skill_level_data = {"generators": generators_data, "skill_level": skill_level}
            if task is not None:
                skill_level_data["task"] = task
            skill_levels_data.append(skill_level_data)

        skill_data = {"skill_levels": skill_levels_data, "skill": skill}
        if choice_task is not None:
            skill_data["choice_task"] = choice_task
        skills_data.append(skill_data)

    template_name = "manage_test.html"
    context = {"stage": stage, "test": test, "skills": skills_data, "test_date": str(test.date)}
    return render(request, template_name, context)


@staff_member_required
def generate_test(request, pk: int):
    template_name = "generate_test.html"
    test = Test.objects.filter(pk=pk).first()
    latex_creator = LatexCreator(test)
    test_str = latex_creator.generate_tests(solution=False)
    answers_str = latex_creator.generate_tests(solution=True)
    context = {"test_str": test_str, "answers_str": answers_str}
    return render(request, template_name, context)


@staff_member_required
def create_student_test(request):
    form = StudentTestForm(None, request.POST or None)
    if form.is_valid():
        student_test = form.save(commit=False)
        student_test.save()
        skill_levels = form.cleaned_data["skill_levels"]
        for skill_level in skill_levels:
            student_test.skill_levels.add(skill_level)
        students = form.cleaned_data["students"]
        for student in students:
            student_test.students.add(student)
        return redirect("../../")
    template_name = "form.html"
    context = {"form": form}
    return render(request, template_name, context)


@staff_member_required
def manage_student_test(request, pk: int):
    if request.POST:
        data = defaultdict(lambda: defaultdict(lambda: {}))
        for key, value in request.POST.items():
            keys = key.split("_")
            if len(keys) == 3:
                data[keys[0]][keys[1]][keys[2]] = value
        student_test = get_object_or_404(StudentTest, pk=int(request.POST["test-id"]))
        test_data = data["test"]["0"]
        if student_test.name != test_data["name"]:
            student_test.name = test_data["name"]
            student_test.save()
        if student_test.write_student_name != test_data.__contains__("write-student-name"):
            student_test.write_student_name = not student_test.write_student_name
            student_test.save()
        if student_test.date != test_data["date"]:
            student_test.date = test_data["date"]
            student_test.save()
        # TODO students
        for task_name, task_data in data["task"].items():
            if task_name.startswith('skilllevel'):
                if task_data['page'] != '':
                    skill_level_id = int(task_name.split('-')[1])
                    skill_level = get_object_or_404(SkillLevel, pk=skill_level_id)
                    generate_all = True if task_data["all"] == "all" else False
                    test_task = TestTask(
                        student_test=student_test, skill_level=skill_level,
                        generate_all=generate_all, page=int(task_data['page']),
                    )
                    test_task.save()
                    for key, value in task_data.items():
                        if key.startswith("generator"):
                            generator = get_object_or_404(TaskGenerator, id=int(value))
                            test_task.generators.add(generator)
            else:
                test_task = get_object_or_404(TestTask, pk=int(task_name))
                generate_all = True if task_data["all"] == "all" else False
                if test_task.generate_all != generate_all:
                    test_task.generate_all = generate_all
                    test_task.save()
                if test_task.page != task_data['page']:
                    test_task.page = task_data['page']
                    test_task.save()
                generator_ids = []
                for key, value in task_data.items():
                    if key.startswith("generator"):
                        generator_ids.append(int(value))
                for generator in test_task.generators.all():
                    if generator.pk not in generator_ids:
                        test_task.generators.remove(generator)
                for id in generator_ids:
                    if not test_task.generators.filter(id=id).first():
                        generator = get_object_or_404(TaskGenerator, id=id)
                        test_task.generators.add(generator)

    student_test = StudentTest.objects.filter(pk=pk).first()
    stage = student_test.stage
    skill_levels = student_test.skill_levels.all().order_by("pk")

    skill_levels_data =[]
    for skill_level in skill_levels:
        task = TestTask.objects.filter(
            skill_level_id=skill_level.pk,
            student_test_id=student_test.pk,
        ).first()
        generators = skill_level.generators.all()
        generators_data = []
        for generator in generators:
            generator_data = {"generator": generator}
            if task is not None:
                if task.generators.filter(id=generator.pk).first():
                    generator_data["checked"] = True
            generators_data.append(generator_data)
        skill_level_data = {"generators": generators_data, "skill_level": skill_level}
        if task is not None:
            skill_level_data["task"] = task
        skill_levels_data.append(skill_level_data)

    template_name = "manage_student_test.html"
    context = {"stage": stage, "test": student_test, "skill_levels": skill_levels_data, "test_date": str(student_test.date)}
    return render(request, template_name, context)


@staff_member_required
def generate_student_test(request, pk: int):
    template_name = "generate_test.html"
    student_test = StudentTest.objects.filter(pk=pk).first()
    latex_creator = LatexCreator(student_test=student_test)
    test_str = latex_creator.generate_tests(solution=False)
    answers_str = latex_creator.generate_tests(solution=True)
    context = {"test_str": test_str, "answers_str": answers_str}
    return render(request, template_name, context)
