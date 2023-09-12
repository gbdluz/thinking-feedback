import functools

from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.shortcuts import redirect

from users.models import Initial_Password


def authentication_not_required(view_func):
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        messages.info(request, "You need to be logged out")
        print("You need to be logged out")
        return redirect("/")

    return wrapper


def email_required(view_func):
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.email:
            return view_func(request, *args, **kwargs)
        messages.info(request, "You need to add your email address")
        return redirect("/update_user/")

    return wrapper


def new_password_required(view_func):
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            initial_passwords = Initial_Password.objects.filter(student=request.user)
            if len(initial_passwords) > 0:
                initial_password = initial_passwords.first().password
                if check_password(initial_password, request.user.password):
                    messages.info(request, "You need to change your password")
                    return redirect("/password/")

        return view_func(request, *args, **kwargs)

    return wrapper
