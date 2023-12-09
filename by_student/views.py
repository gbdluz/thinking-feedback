from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.timezone import now

from classes.models import Stage
from topic.models import Topic, Skill
from grade.models import Grade


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


convert_grade = lambda grade: "ok" if grade.value == "tick" else "nie" if grade.value == "cross" else grade.value


def get_passed_levels(levels):
    passed_levels = []
    for level, g in levels.items():
        convert = lambda val: "✔" if val == "tick" else "✘" if val == "cross" else val
        g_str = ''.join([convert(grade.value) for grade in g])
        streaks = g_str.split("✘")
        passed = False
        for streak in streaks:
            if len(streak) == 2 and streak[0] == "✔" and streak[1] == "✔":
                passed = True
            if len(streak) >= 3 and streak.__contains__("✔"):
                passed = True
        if passed:
            passed_levels.append(int(level))
    return passed_levels


@staff_member_required
def by_student_view(request, pk1):
    student = User.objects.get(pk=pk1)
    stage = student.classes.all()[0]
    if stage.teacher != request.user:
        return redirect("/")
    topics = Topic.objects.filter(stage=stage)
    topic_grades = {}
    context = {
        "student": student,
    }
    table = ""
    for topic in topics:
        table += "Dział " + topic.title + ": \n"
        skill_list = Skill.objects.filter(topic=topic).order_by("order")
        grades = {}
        student = User.objects.get(pk=pk1)
        for skill in skill_list:
            table += skill.title + ": "
            grades[skill] = []
            levels = {}
            for level in skill.levels.all():
                levels[level.level] = []
                temp = Grade.objects.filter(student=student, skill_level=level).order_by("publish_date")
                for grade in temp:
                    levels[level.level].append(grade)
            passed_levels = get_passed_levels(levels)
            max_passed_level = 0
            if len(passed_levels) > 0:
                max_passed_level = max(passed_levels)
            for level, g in sorted(levels.items(), key=lambda x: x[0]):
                if int(level) <= max_passed_level:
                    g.append(Grade(value="(zal)", publish_date=now()))
                grades[skill].append(g)
                if len(g) > 0 and g[-1].value == "(zal)":
                    table += f"(p{level}: ZAL);"
                else:
                    table += f"(p{level}: " + ", ".join([convert_grade(grade) for grade in g[:-1]]) + "); "
            table += "\n"
            topic_grades[topic.title] = grades
    table += """Legenda:
p1 - informacje o podejściach z poziomu pierwszego (odpowiednio 2 i 3 to drugi i trzeci poziom),
ok - jedno podejście zakończone sukcesem,
B - jedno podejście z błędem,
nie - jedno podejście niepoprawne,
ZAL - umiejętność zaliczona na tym poziomie."""
    context["grades"] = topic_grades
    context["table"] = table
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
    }
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
