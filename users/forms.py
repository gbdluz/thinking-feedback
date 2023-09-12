from django import forms
from django.contrib.auth.forms import (
    PasswordChangeForm, PasswordResetForm,
    SetPasswordForm,
)
from django.contrib.auth.models import User


class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "type": "password"}),
    )
    new_password1 = forms.CharField(
        max_length=100,
        widget=forms.PasswordInput(attrs={"class": "form-control", "type": "password"}),
    )
    new_password2 = forms.CharField(
        max_length=100,
        widget=forms.PasswordInput(attrs={"class": "form-control", "type": "password"}),
    )

    class Meta:
        model = User
        fields = ["old_password", "new_password1", "new_password2"]


class PasswordSettingForm(SetPasswordForm):
    new_password1 = forms.CharField(
        max_length=100,
        widget=forms.PasswordInput(attrs={"class": "form-control", "type": "password"}),
    )
    new_password2 = forms.CharField(
        max_length=100,
        widget=forms.PasswordInput(attrs={"class": "form-control", "type": "password"}),
    )

    class Meta:
        model = User
        fields = ["new_password1", "new_password2"]


class PasswordResettingForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(PasswordResettingForm, self).__init__(*args, **kwargs)

        # self.fields['email'].widget.attrs['class'] = 'form-control'

    email = forms.EmailField(
        label="",
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Your email",
                "type": "email",
                "name": "email",
            },
        ),
    )
