from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path

from .forms import PasswordResettingForm
from .views import (
    PasswordsChangeView, PasswordSettingView,
    home_page, login_page, logout_page, password_success,
    register, update_user,
)

urlpatterns = [
    path("", home_page, name="home"),
    path("login/", include("django.contrib.auth.urls")),
    path("login/", login_page),
    path("logout/", logout_page),
    path("register/", register),
    path("update_user/", update_user),
    path("password/", PasswordsChangeView.as_view(template_name="form.html")),
    path("password/success/", password_success, name="password_success"),
    path(
        "reset_password/",
        auth_views.PasswordResetView.as_view(
            template_name="password_reset.html", form_class=PasswordResettingForm,
        ),
        name="reset_password",
    ),
    path(
        "reset_password_sent/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="password_reset_sent.html",
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        PasswordSettingView.as_view(template_name="password_reset_form.html"),
        name="password_reset_confirm",
    ),
    path(
        "reset_password_complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="password_reset_done.html",
        ),
        name="password_reset_complete",
    ),
]

urlpatterns += staticfiles_urlpatterns()
