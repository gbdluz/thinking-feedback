from django import forms

from classes.models import Stage


class StageEditForm(forms.ModelForm):
    class Meta:
        model = Stage
        fields = ["title"]
