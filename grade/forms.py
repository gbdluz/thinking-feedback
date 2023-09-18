from bootstrap_modal_forms.forms import BSModalModelForm
from django import forms
from django.contrib.auth.models import User
from django.forms import formset_factory

from classes.models import Stage
from grade.models import Grade, MARK_CHOICES, TYPE_CHOICES
from topic.models import Skill


class StageTopicsStudentsForm(forms.Form):
    stage = forms.ModelChoiceField(queryset=Stage.objects.all(), widget=forms.Select)
    skills = forms.ModelMultipleChoiceField(required=False, queryset=Skill.objects.all(), widget=forms.CheckboxSelectMultiple)
    students = forms.ModelMultipleChoiceField(required=False, queryset=User.objects.all(), widget=forms.CheckboxSelectMultiple(attrs={"checked":""}))
    default_mark = forms.ChoiceField(choices=MARK_CHOICES, required=False)
    default_type = forms.ChoiceField(choices=TYPE_CHOICES, required=False)

    stage.widget.attrs.update({"onchange": "if(this.value != 0) { this.form.submit(); }"})

    def __init__(self, user, *args, stage=None, **kwargs):
        super(StageTopicsStudentsForm, self).__init__(*args, **kwargs)
        self.fields["stage"].queryset = Stage.objects.filter(teacher=user)
        if stage is not None:
            self.fields["skills"].queryset = Skill.objects.filter(topic__stage_id=stage.pk)
            self.fields["students"].queryset = stage.students


# TODO: use one of below
class GradeModelForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ["student", "skill_level", "value", "type", "comment"]

    def __init__(self, *args, **kwargs):
        super(GradeModelForm, self).__init__(*args, **kwargs)
        self.fields["comment"].required = False


class GradeModalModelForm(BSModalModelForm):
    class Meta:
        model = Grade
        fields = ["student", "skill_level", "value", "type", "comment"]
