from collections import defaultdict
import datetime

from django import forms
from django.contrib.auth.models import User

from classes.models import Stage
from exam.models import Test, StudentTest
from exam.widgets import GroupedCheckboxSelectMultiple
from topic.models import Skill, SkillLevel


class StageForm(forms.Form):
    stage = forms.ModelChoiceField(queryset=Stage.objects.all(), widget=forms.Select)

    stage.widget.attrs.update({"onchange": "if(this.value != 0) { this.form.submit(); }"})


class TestForm(forms.ModelForm):
    skills = forms.ModelMultipleChoiceField(queryset=Skill.objects.all(), widget=GroupedCheckboxSelectMultiple())
    date = forms.DateField(initial=datetime.date.today().strftime('%d-%m-%Y'), widget=forms.DateInput(format="%d-%m-%Y", attrs={'type': 'date'}))

    class Meta:
        model = Test
        fields = ["name", "stage", "skills", "date"]

    def __init__(self, stage, *args, **kwargs):
        super(TestForm, self).__init__(*args, **kwargs)
        if stage is not None:
            self.fields["stage"].initial = stage
            self.fields["stage"].queryset = Stage.objects.filter(id=stage.pk)
            skills = Skill.objects.filter(topic__stage_id=stage.pk)
            topic_to_skill = defaultdict(list)
            for skill in skills:
                topic_to_skill[skill.topic].append(skill)
            topic_to_skill_tuples = [
                (topic.title, [(skill.pk, skill) for skill in sorted(skills, key=lambda sk: (sk.topic.pk, sk.order))])
                for topic, skills in sorted(topic_to_skill.items(), key=lambda k: k[0].pk)
            ]
            self.fields["skills"].choices = topic_to_skill_tuples


class StudentTestForm(forms.ModelForm):
    skill_levels = forms.ModelMultipleChoiceField(queryset=SkillLevel.objects.all(), widget=GroupedCheckboxSelectMultiple())
    students = forms.ModelMultipleChoiceField(queryset=User.objects.all(), widget=GroupedCheckboxSelectMultiple())
    date = forms.DateField(initial=datetime.date.today().strftime('%d-%m-%Y'), widget=forms.DateInput(format="%d-%m-%Y", attrs={'type': 'date'}))

    class Meta:
        model = StudentTest
        fields = ["name", "stage", "students", "skill_levels", "date", "write_student_name"]

    def __init__(self, stage, *args, **kwargs):
        super(StudentTestForm, self).__init__(*args, **kwargs)
        if stage is not None:
            self.fields["stage"].initial = stage
            self.fields["stage"].queryset = Stage.objects.filter(id=stage.pk)
            students = User.objects.filter(classes__id=stage.pk)
            self.fields["students"].choices = [
                ("Uczniowie", [(user.pk, user) for user in students]),
            ]
            skill_levels = SkillLevel.objects.filter(skills__topic__stage_id=stage.pk)
            topic_to_skill_levels = defaultdict(list)
            for skill_level in skill_levels:
                topic_to_skill_levels[skill_level.skills.first().topic].append(skill_level)
            topic_to_skill_levels_tuples = [
                    (
                        topic.title, [(skill_level.pk, skill_level) for skill_level
                        in sorted(skill_levels, key=lambda lvl: (min(sk.order for sk in lvl.skills.all()), lvl.level))],
                    )
                for topic, skill_levels in sorted(topic_to_skill_levels.items(), key=lambda k: k[0].pk)
            ]
            self.fields["skill_levels"].choices = topic_to_skill_levels_tuples
