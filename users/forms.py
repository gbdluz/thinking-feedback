from django import forms
from django.contrib.auth.forms import (
    PasswordChangeForm, PasswordResetForm,
    SetPasswordForm, UserCreationForm,
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


class StudentForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name"]

    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)

        self.fields["first_name"].widget.attrs["class"] = "form-control"
        self.fields["last_name"].widget.attrs["class"] = "form-control"


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
            },
        ),
    )
    last_name = forms.CharField(
        max_length=100, widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        ]

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields["username"].widget.attrs["class"] = "form-control"
        self.fields["password1"].widget.attrs["class"] = "form-control"
        self.fields["password2"].widget.attrs["class"] = "form-control"


class UpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email"]

    def __init__(self, *args, **kwargs):
        super(UpdateForm, self).__init__(*args, **kwargs)

        self.fields["username"].widget.attrs["class"] = "form-control"
        print(self.fields["username"].widget.attrs)
        self.fields["email"].widget.attrs["class"] = "form-control"
