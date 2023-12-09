from bootstrap_modal_forms.forms import BSModalModelForm
from django import forms
from django.contrib.auth.models import User

from classes.models import Stage
from exam.models import Test, StudentTest
from grade.models import Grade, MARK_CHOICES, TYPE_CHOICES
from topic.models import Skill

ADD_GRADE_TYPES = (("test", "Dodaj oceny do testu"), ("student_test", "Dodaj oceny do poprawy"), ("topic_students", "Dodaj inne oceny"))


class StageForm(forms.Form):
    stage = forms.ModelChoiceField(queryset=Stage.objects.all(), widget=forms.Select)
    add_grade_type = forms.ChoiceField(choices=ADD_GRADE_TYPES, widget=forms.Select)

    def __init__(self, user, *args, **kwargs):
        super(StageForm, self).__init__(*args, **kwargs)
        self.fields["stage"].queryset = Stage.objects.filter(teacher=user)


class StageTopicsStudentsForm(forms.Form):
    stage = forms.ModelChoiceField(queryset=Stage.objects.all(), widget=forms.Select)
    skills = forms.ModelMultipleChoiceField(queryset=Skill.objects.all(), widget=forms.CheckboxSelectMultiple)
    students = forms.ModelMultipleChoiceField(queryset=User.objects.all(), widget=forms.CheckboxSelectMultiple(attrs={"checked":""}))
    default_mark = forms.ChoiceField(choices=MARK_CHOICES)
    default_type = forms.ChoiceField(choices=TYPE_CHOICES)

    def __init__(self, stage, *args, **kwargs):
        super(StageTopicsStudentsForm, self).__init__(*args, **kwargs)
        self.fields["stage"].queryset = Stage.objects.filter(id=stage.pk)
        self.fields["stage"].initial = stage
        self.fields["skills"].queryset = Skill.objects.filter(topic__stage_id=stage.pk)
        self.fields["students"].queryset = stage.students


class StageTestForm(forms.Form):
    stage = forms.ModelChoiceField(queryset=Stage.objects.all(), widget=forms.Select)
    test = forms.ModelChoiceField(queryset=Test.objects.all(), required=False)

    def __init__(self, stage, *args, **kwargs):
        super(StageTestForm, self).__init__(*args, **kwargs)
        self.fields["stage"].queryset = Stage.objects.filter(id=stage.pk)
        self.fields["stage"].initial = stage
        self.fields["test"].queryset = Test.objects.filter(stage_id=stage.pk)


class StageStudentTestForm(forms.Form):
    stage = forms.ModelChoiceField(queryset=Stage.objects.all(), widget=forms.Select)
    student_test = forms.ModelChoiceField(queryset=StudentTest.objects.all(), required=False)

    def __init__(self, stage, *args, **kwargs):
        super(StageStudentTestForm, self).__init__(*args, **kwargs)
        self.fields["stage"].queryset = Stage.objects.filter(id=stage.pk)
        self.fields["stage"].initial = stage
        self.fields["student_test"].queryset = StudentTest.objects.filter(stage_id=stage.pk)


class GradeModelForm(forms.ModelForm):
    grade_id = forms.IntegerField(required=False)

    class Meta:
        model = Grade
        fields = ["student", "skill_level", "value", "type", "comment", "test", "student_test"]

    def __init__(self, *args, **kwargs):
        super(GradeModelForm, self).__init__(*args, **kwargs)
        self.fields["comment"].required = False
        self.fields["test"].required = False
        self.fields["student_test"].required = False


class DeleteGradeForm(forms.Form):
    grade_id = forms.IntegerField(required=False)


# TODO: remove
class GradeModalModelForm(BSModalModelForm):
    class Meta:
        model = Grade
        fields = ["student", "skill_level", "value", "type", "comment"]
