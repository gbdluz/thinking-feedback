from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from topic.models import Grade, Skill, Topic
from users.decorators import email_required, new_password_required


# Create your views here.
@login_required
@email_required
@new_password_required
def student_topics(request):
    if request.user.is_staff:
        return redirect("/")
    qs = Topic.objects.filter(stage=request.user.your_stage.stage)
    context = {"topic_list": qs}
    template_name = "student_topics.html"
    return render(request, template_name, context)


@login_required
@email_required
@new_password_required
def student_detail(request, pk):
    if request.user.is_staff:
        return redirect("/")
    obj = get_object_or_404(Topic, pk=pk)
    skill_list = Skill.objects.filter(topic=obj)
    context = {
        "skill_list": skill_list,
        "title": "",
        "topic": obj.title,
    }  #'slug': slug,
    grades = {}
    student = request.user
    for skill in skill_list:
        grades[skill] = {}
        for level in (1, 2, 3):
            grades[skill][level] = []
            temp = Grade.objects.filter(student=student, skill=skill, level=level)
            for grade in temp:
                grades[skill][level].append(grade)
    print(grades)
    context["grades"] = grades
    template_name = "student_detail.html"
    return render(request, template_name, context)
