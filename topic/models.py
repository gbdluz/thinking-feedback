from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_delete

# Create your models here.
from classes.models import Stage
from task.models import Task, TaskGenerator


class Topic(models.Model):
    title = models.CharField(max_length=120)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return f"/topic/{self.pk}"

    def get_update_url(self):
        return f"/topic/{self.pk}/edit/"

    def get_add_skill_url(self):
        return f"/topic/{self.pk}/add/"

    def get_delete_url(self):
        return f"/topic/{self.pk}/delete/"

    def __str__(self):
        return self.title


class Skill(models.Model):
    title = models.CharField(max_length=120)
    topic = models.ForeignKey(Topic, default=1, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return f"/topic/{self.topic.pk}/skill/{self.pk}"

    def get_edit_url(self):
        return f"/topic/{self.topic.pk}/skill/{self.pk}/edit"

    def get_delete_url(self):
        return f"/topic/{self.topic.pk}/skill/{self.pk}/delete"

    def get_grade_edit_url(self):
        return f"/topic/{self.topic.pk}/skill/{self.pk}/grade_edit"

    def get_grade_delete_url(self):
        return f"/topic/{self.topic.pk}/skill/{self.pk}/grade_delete"

    def __str__(self):
        return self.title


class SkillLevel(models.Model):
    skills = models.ManyToManyField(Skill, related_name="levels")
    level = models.CharField(
        max_length=1,
        choices=(("1", "Chill"), ("2", "Medium"), ("3", "Challenge")),
        default=1,
    )
    example_task = models.ForeignKey(Task, default=1, on_delete=models.CASCADE)
    tasks = models.ManyToManyField(Task, related_name="skill_levels")
    generators = models.ManyToManyField(TaskGenerator, related_name="skill_levels")


# What happens here??
def delete_students(sender, instance, **kwargs):
    students = get_user_model().objects.filter(your_stage=None, is_staff=False)
    for student in students:
        student.delete()


post_delete.connect(delete_students, sender=Stage)
