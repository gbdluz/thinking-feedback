from django.contrib.auth.models import User
from django.db import models

from classes.models import Stage
from task.models import TaskGenerator
from topic.models import SkillLevel, Skill


class TestTask(models.Model):
    student_test = models.ForeignKey("StudentTest", null=True, on_delete=models.SET_NULL)
    skill_level = models.ForeignKey(SkillLevel, default=1, on_delete=models.SET_DEFAULT)
    choice_test_task = models.ForeignKey("ChoiceTestTask", null=True, on_delete=models.SET_NULL)
    generators = models.ManyToManyField(TaskGenerator, related_name="test_tasks")
    generate_all = models.BooleanField(default=True)
    page = models.IntegerField(default=2)


class ChoiceTestTask(models.Model):
    test = models.ForeignKey("Test", null=True, on_delete=models.SET_NULL)
    skill = models.ForeignKey(Skill, default=1, on_delete=models.SET_DEFAULT)
    page = models.IntegerField(default=2)


class Test(models.Model):
    name = models.CharField(max_length=40)
    stage = models.ForeignKey(Stage, default=1, on_delete=models.SET_DEFAULT)
    skills = models.ManyToManyField(Skill, related_name="tests")
    groups = models.IntegerField(default=2)
    group_number = models.IntegerField(default=1)
    date = models.DateField()

    def get_manage_url(self):
        return f"/test/{self.pk}/manage"

    def __str__(self):
        return self.name


class StudentTest(models.Model):
    name = models.CharField(max_length=40)
    stage = models.ForeignKey(Stage, default=1, on_delete=models.SET_DEFAULT)
    students = models.ManyToManyField(User, related_name="student_tests")
    skill_levels = models.ManyToManyField(SkillLevel, related_name="student_tests")
    date = models.DateField()
    group_number = models.IntegerField(default=1)
    write_student_name = models.BooleanField(default=True)

    def get_manage_url(self):
        return f"/test/student/{self.pk}/manage"

    def __str__(self):
        return self.name
