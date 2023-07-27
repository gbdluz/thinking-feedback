from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView, PasswordResetConfirmView, PasswordResetDoneView
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, PasswordResetForm
from django.urls import reverse_lazy
from django import forms


# Create your views here.
from .models import Topic, Skill, Grade, Stage, Your_Stage, Initial_Password
from .forms import TopicModelForm, SkillModelForm, SignUpForm, PasswordChangingForm, PasswordSettingForm, PasswordResettingForm, UpdateForm
from thinking_feedback.views import home_page

context = {}

class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangingForm
    success_url = reverse_lazy('password_success')

@login_required
def password_success(request):
    messages.success(request, message="Your password has been changed.")
    return redirect('/')

class PasswordResettingView(PasswordResetDoneView):
    form_class = PasswordResettingForm
    success_url = reverse_lazy('password_reset_done')


class PasswordSettingView(PasswordResetConfirmView):
    form_class = PasswordSettingForm
    success_url = reverse_lazy('password_reset_complete')


def register(request):
    form = SignUpForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.is_staff = True
        obj.save()
        stage = Your_Stage()
        stage.user = obj
        stage.role = 'TEACHER'
        stage.save()
        obj.your_stage = stage 
        obj.save()
        login(request, obj)
        return redirect('/')
    template_name = 'form.html'
    context = {'title': 'Register', 'form': form}
    return render(request, template_name, context)

@login_required
def update_user(request):
    user = request.user
    form = UpdateForm(request.POST or None, instance=user)
    if form.is_valid():
        obj = form.save(commit=False)
        user.username = obj.username
        user.password = obj.password
        user.save()
        login(request, user)
        return redirect('/')
    template_name = 'update_user.html'
    context = {'user': user, 'title': 'Update your details', 'form': form}
    return render(request, template_name, context)


@staff_member_required
def topic_list_view(request):
    qs = Topic.objects.filter(teacher=request.user)

    template_name = 'topic_list.html'
    context = {'object_list': qs, 'topic_list': qs}
    return render(request, template_name, context)


@staff_member_required
def by_subject(request):
    stages = Stage.objects.filter(teacher=request.user)
    context['stages'] = stages

    topics = {}
    for stage in stages:
        temp = Topic.objects.filter(stage=stage)
        topics[stage] = temp
    context['topics'] = topics
    context['empty'] = 0
    if len(stages) == 0:
        context['empty'] = 1

    template_name = 'by_subject.html'
    return render(request, template_name, context)

@staff_member_required
def topic_detail_view(request, slug):
    stages  = Stage.objects.filter(teacher=request.user)
    obj     = get_object_or_404(Topic, slug=slug, stage__in=stages)

    qs2 = Skill.objects.filter(topic = obj)
    template_name = 'topic_detail.html'
    context= {"object": obj, "skill_list": qs2}
    context['empty'] = 0
    if len(qs2) == 0:
        context['empty'] = 1
    return render(request, template_name, context)

@staff_member_required
def add_topic(request):
    user     = request.user
    form     = TopicModelForm(user, request.POST or None)
    if form.is_valid():
        obj  = form.save(commit = False)
        obj.teacher = request.user
        obj.save()
        user = request.user
        form = TopicModelForm(user)
        return redirect('/topic')
    template_name = 'form.html'
    context  = {'form': form}
    return render(request, template_name, context)

@staff_member_required
def add_skill(request, slug):
    stages  = Stage.objects.filter(teacher=request.user)
    form    = SkillModelForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit = False)
        topic = get_object_or_404(Topic, slug = slug, stage__in=stages)
        obj.topic = topic
        obj.save()
        return redirect('..')
    template_name = 'form.html'
    context = {'form': form}
    return render(request, template_name, context)

@staff_member_required
def update_topic(request, slug):
    user = request.user
    stages  = Stage.objects.filter(teacher=request.user)
    topic = get_object_or_404(Topic, slug=slug, stage__in=stages)
    form = TopicModelForm(user, request.POST or None, instance=topic)
    if form.is_valid():
        obj  = form.save(commit = False)
        obj.teacher = request.user
        obj.save()
        user = request.user
        form = TopicModelForm(user)
        return redirect('..')
    template_name = 'form.html'
    context  = {'form': form}
    return render(request, template_name, context)

@staff_member_required
def delete_topic(request, slug):
    stages  = Stage.objects.filter(teacher=request.user)
    topic = get_object_or_404(Topic, slug=slug, stage__in=stages)
    if request.method == "POST":
        topic.delete()
        return redirect('../..')
    template_name = 'delete_topic.html'
    context = {'topic': topic}
    return render(request, template_name, context)


@staff_member_required
def skill_update(request, slug1, slug2):
    stages = Stage.objects.filter(teacher=request.user)
    topic  = get_object_or_404(Topic, slug=slug1, stage__in=stages)
    skill  = get_object_or_404(Skill, slug=slug2)
    stage  = topic.stage
    template_name = 'skill_update.html'
    std_stages = Your_Stage.objects.filter(stage=stage)
    students   = User.objects.filter(your_stage__in=std_stages)
    context = {'topic': topic, 'skill': skill, 'stage': stage, 'students': students}    

    
    if request.POST:
        for key in request.POST.keys():
            if key != 'csrfmiddlewaretoken' and key != 'level':
                student = User.objects.get(pk = key)
                value   = request.POST[key]
                level   = request.POST['level']
                grade   = Grade(student=student, skill=skill, value=value, level=level)
                grade.save()
        return redirect('..')
    return render(request, template_name, context)

@staff_member_required
def skill_edit(request, slug1, slug2):
    stages = Stage.objects.filter(teacher=request.user)
    topic  = get_object_or_404(Topic, slug=slug1, stage__in=stages)
    skill  = get_object_or_404(Skill, slug=slug2)
    form    = SkillModelForm(request.POST or None, instance=skill)
    if form.is_valid():
        obj = form.save(commit = False)
        # topic = get_object_or_404(Topic, slug = slug1, stage__in=stages)
        obj.topic = topic
        obj.save()
        return redirect(f'../../{obj.slug}')
    template_name = 'form.html'
    context = {'form': form}
    return render(request, template_name, context)


@staff_member_required
def skill_delete(request, slug1, slug2):
    stages = Stage.objects.filter(teacher=request.user)
    topic  = get_object_or_404(Topic, slug=slug1, stage__in=stages)
    skill  = get_object_or_404(Skill, slug=slug2)
    if request.method == "POST":
        skill.delete()
        return redirect('../../..')
    template_name = 'delete_skill.html'
    context = {'skill': skill}
    return render(request, template_name, context)

@staff_member_required
def list_students(request):
    stages   = Stage.objects.filter(teacher=request.user)
    students = {}
    for stage in stages:
        temp = Your_Stage.objects.filter(stage=stage)
        std  = User.objects.filter(your_stage__in=temp)
        students[stage] = std
    context['students'] = students
    context['empty'] = 0
    if len(students) == 0:
        context['empty'] = 1
    template_name = 'list_students.html'
    return render(request, template_name, context)

@staff_member_required
def view_passwords(request, pk):
    stage = Stage.objects.get(pk=pk, teacher=request.user)
    your_stages = Your_Stage.objects.filter(stage=stage)
    students = User.objects.filter(your_stage__in=your_stages)
    passwords = Initial_Password.objects.filter(student__in=students)
    # stage = get_object_or_404(Stage, pk=pk, teacher=request.user)
    # passwords = stage.passwords
    # qs = Your_Stage.objects.filter(stage=stage)
    # qs2 = User.objects.filter(your_stage__in=qs)
    # print(stage, stage.teacher, stage.passwords
    print(stage)
    print(students)
    print(passwords)
    context = {'stage': stage, 'passwords': passwords} #, 'passwords': passwords
    template_name = 'view_passwords.html'
    return render(request, template_name, context)



@staff_member_required
def add_class(request):
    context = {}
    template_name = "add_class.html"
    if request.POST:
        stage_name  = request.POST['stage_name']
        size        = request.POST['size']
        new_stage   = Stage()
        new_stage.title     = stage_name
        new_stage.teacher   = request.user
        new_stage.number    = size
        new_stage.save()
        pk = new_stage.pk
        return redirect(f"/your_classes/add/next/{new_stage.pk}")
    return render(request, template_name, context)

@staff_member_required
def add_class_next(request, pk):
    stage       = Stage.objects.get(pk=pk)
    students    = Your_Stage.objects.filter(stage=stage)
    if students:
        return redirect('/') 
    else:
        range_ = range(stage.number)
        context = {'size': stage.number, 'name': stage.title, 'range_': range_}
        template_name = 'add_class_next.html'
        if request.POST:
            passwords = {}
            for idx in range_:
                first_name = request.POST[str(idx)+'.first_name'].strip()
                last_name = request.POST[str(idx)+'.last_name'].strip()
                username = (first_name[:min(3, len(first_name))].strip() + last_name[:min(4, len(last_name))].strip()).lower()
                counter = 1
                while User.objects.filter(username=username):
                    username = first_name + str(counter)
                    counter += 1
                student = User.objects.create_user(username=username, first_name=first_name, last_name=last_name)
                student.save()
                password = User.objects.make_random_password()
                student.set_password(password)
                student.save()
                passwords[student] = password
                your_stage = Your_Stage()
                your_stage.user = student
                your_stage.role = 'STUDENT'
                your_stage.stage = stage
                your_stage.save()
                student.your_stage = your_stage
                student.save()
                Initial_Password.objects.create(student=student, password=password)
            stage.passwords = passwords
            # print(stage, stage.passwords)
            return add_class_next_next(request, passwords)
            # return redirect('/')
        return render(request, template_name, context)
    
@staff_member_required
def add_class_next_next(request, passwords):
    template_name = "add_class_next_next.html"
    context = {'passwords': passwords}
    return render(request, template_name, context)
    

@login_required
def student_topics(request):
    if request.user.is_staff:
        return redirect('/')
    qs      = Topic.objects.filter(stage = request.user.your_stage.stage)
    context = {'topic_list': qs}
    template_name = 'student_topics.html'
    return render(request, template_name, context)

@login_required
def student_detail(request, slug):
    if request.user.is_staff:
        return redirect('/')
    obj = get_object_or_404(Topic, slug = slug)
    skill_list = Skill.objects.filter(topic = obj)
    context['skill_list']   = skill_list
    context['slug']         = slug
    context['title']        = ''
    context['topic']        = obj.title
    grades = {}
    student = request.user
    for skill in skill_list:   
        grades[skill] = {}
        for level in (1,2,3):
            grades[skill][level] = []
            temp = Grade.objects.filter(student=student, skill=skill, level=level)
            for grade in temp:
                grades[skill][level].append(grade.value)
    print(grades)
    context['grades'] = grades
    template_name   = 'student_detail.html'
    return render(request, template_name, context)

@staff_member_required
def by_student(request):
    stages = Stage.objects.filter(teacher=request.user)
    students = {}
    for stage in stages:
        temp = Your_Stage.objects.filter(stage=stage)
        std  = User.objects.filter(your_stage__in=temp)
        students[stage] = std
    context['students'] = students
    context['empty'] = 0
    if len(stages) == 0:
        context['empty'] = 1
    template_name = 'by_student.html'
    return render(request, template_name, context)

@staff_member_required
def by_student_pick_topic(request, pk):
    student = User.objects.get(pk=pk)
    stage   = student.your_stage.stage
    if stage.teacher != request.user:
        return redirect('/')
    qs      = Topic.objects.filter(stage=stage)
    context = {'topic_list': qs, 'student': student, 'stage': stage}
    template_name = "by_student_pick_topic.html"
    return render(request, template_name, context)

@staff_member_required
def by_student_view(request, pk, slug):
    student     = User.objects.get(pk=pk)
    stage       = student.your_stage.stage
    if stage.teacher != request.user:
        return redirect('/')
    obj         = get_object_or_404(Topic, slug = slug)
    skill_list  = Skill.objects.filter(topic = obj)
    context['skill_list'] = skill_list
    context['slug'] = slug
    context['student'] = student
    context['topic'] = obj.title
    grades  = {}
    student = User.objects.get(pk=pk)
    for skill in skill_list:   
        grades[skill] = {}
        for level in (1,2,3):
            grades[skill][level] = []
            temp = Grade.objects.filter(student=student, skill=skill, level=level)
            for grade in temp:
                grades[skill][level].append(grade.value)
    print(grades)
    context['grades'] = grades
    template_name = "by_student_view.html"
    return render(request, template_name, context)

@staff_member_required
def by_student_update(request, pk, slug):
    obj         = get_object_or_404(Topic, slug=slug)
    student     = User.objects.get(pk = pk)
    stage       = student.your_stage.stage
    if stage.teacher != request.user:
        return redirect('/')
    skill_list  = Skill.objects.filter(topic=obj)
    context['student']         = student
    context['skill_list']   = skill_list
    context['topic']        = obj.title
    template_name = 'by_student_update.html'
    if request.POST:
        for key, value in request.POST.items():
            if key != 'csrfmiddlewaretoken' and value != 'empty':
                skill_slug=key[:-1]
                skill = Skill.objects.get(topic=obj, slug=skill_slug)
                level = key[-1]
                grade = Grade(student=student, skill=skill, value=value, level=level)
                grade.save()
        return redirect('..')
    return render(request, template_name, context)