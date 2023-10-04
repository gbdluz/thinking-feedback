from django import forms
from django.forms import Textarea

from task.models import Task, TaskGenerator


class TaskModelForm(forms.ModelForm):
    task_type = forms.TextInput()
    content = forms.CharField(
        max_length=500,
        required=False,
    )
    source = forms.CharField(
        max_length=100,
        required=False,
    )

    class Meta:
        model = Task
        fields = ["content", "source"]


class TaskGeneratorModelForm(forms.ModelForm):
    class Meta:
        model = TaskGenerator
        fields = ["code"]
        widgets = {
            "code": Textarea(attrs={"cols": 80, "rows": 20}),
        }
