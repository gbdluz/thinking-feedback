# Create your views here.
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import (
    PasswordChangeView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
)
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy

from classes.models import Stage
from .decorators import (
    authentication_not_required, email_required,
    new_password_required,
)
from .forms import (
    PasswordChangingForm, PasswordResettingForm,
    PasswordSettingForm, SignUpForm, UpdateForm, StudentForm,
)
from .models import InitialPassword


@email_required
@new_password_required
def home_page(request):
    return render(request, "title.html", {"title": f"Welcome to ThinkingFeedback!"})


def login_page(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        template_name = "login.html"
        # context = {'topic_list': qs}
        context = {}
        if request.method == "POST":
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                messages.success(
                    request, message="There was an error logging in. Try again",
                )
                return redirect("/login")
        else:
            return render(request, template_name, context)


def logout_page(request):
    logout(request)
    messages.success(request, message="You were logged out")
    return redirect("/")


@authentication_not_required
def register(request):
    form = SignUpForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.is_staff = True
        obj.save()
        obj.save()
        login(request, obj)
        return redirect("/")
    template_name = "form.html"
    context = {"title": "Register", "form": form}
    return render(request, template_name, context)


class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangingForm
    success_url = reverse_lazy("password_success")


@login_required
def password_success(request):
    messages.success(request, message="Your password has been changed.")
    return redirect("/")


class PasswordResettingView(PasswordResetDoneView):
    form_class = PasswordResettingForm
    success_url = reverse_lazy("password_reset_done")


class PasswordSettingView(PasswordResetConfirmView):
    form_class = PasswordSettingForm
    success_url = reverse_lazy("password_reset_complete")


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
        return redirect("/password/")
    template_name = "update_user.html"
    context = {"user": user, "title": "Update your details", "form": form}
    return render(request, template_name, context)


@staff_member_required
def edit_student(request, pk1, pk2):
    stage = get_object_or_404(Stage, pk=pk1, teacher=request.user)
    student = get_object_or_404(User, pk=pk2)
    form = StudentForm(request.POST or None, instance=student)
    if form.is_valid():
        form.save()
        return redirect("/your_classes")
    template_name = "form.html"
    context = {"form": form}
    return render(request, template_name, context)


@staff_member_required
def delete_student(request, pk1, pk2):
    stage = get_object_or_404(Stage, pk=pk1, teacher=request.user)
    student = get_object_or_404(User, pk=pk2)
    if request.method == "POST":
        student.delete()
        return redirect("/your_classes")
    template_name = "delete_student.html"
    context = {"stage": stage, "student": student}
    return render(request, template_name, context)


@staff_member_required
def add_student(request, pk):
    stage = get_object_or_404(Stage, pk=pk, teacher=request.user)
    form = StudentForm(request.POST or None)
    if form.is_valid():
        student = form.save(commit=False)
        first_name = student.first_name
        last_name = student.last_name
        username = (
            first_name[: min(3, len(first_name))].strip()
            + last_name[: min(4, len(last_name))].strip()
        ).lower()
        student.username = username
        counter = 1
        while User.objects.filter(username=username):
            username = first_name + str(counter)
            counter += 1
        student.save()
        password = User.objects.make_random_password()
        student.set_password(password)
        student.save()
        stage.students.add(student)
        stage.save()
        InitialPassword.objects.create(student=student, password=password)
        return redirect("/your_classes")
    context = {"stage": stage, "form": form}
    template_name = "add_student.html"
    return render(request, template_name, context)
