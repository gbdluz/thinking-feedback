from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
)
from django.contrib.auth.models import User

from .models import Skill, Stage, Topic


class TopicModelForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ["title", "stage"]  #'slug',

    def __init__(self, user, *args, **kwargs):
        super(TopicModelForm, self).__init__(*args, **kwargs)
        print(user)
        self.fields["stage"].queryset = Stage.objects.filter(teacher=user)


class SkillModelForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ["title"]  # , 'slug'


class StageEditForm(forms.ModelForm):
    class Meta:
        model = Stage
        fields = ["title"]


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
