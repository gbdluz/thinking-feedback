# Create your views here.
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import (
    PasswordChangeView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
)
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from topic.forms import SignUpForm, UpdateForm

from .decorators import (
    authentication_not_required, email_required,
    new_password_required,
)
from .forms import (
    PasswordChangingForm, PasswordResettingForm,
    PasswordSettingForm,
)


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
