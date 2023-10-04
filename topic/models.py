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

    def get_edit_whole_topic_url(self):
        return f"/topic/{self.pk}"

    def get_student_view_url(self):
        return f"/topic/{self.pk}/view/"

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
    required_passes = models.IntegerField(default=1)
    order = models.IntegerField()

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

    def get_add_skill_level_url(self):
        return f"/topic/{self.topic.pk}/skill/{self.pk}/add_skill_level"

    def get_change_skill_order_url(self):
        return f"/topic/{self.topic.pk}/skill/{self.pk}/change_order/"

    def __str__(self):
        return f"{self.title} ({self.topic.title})"


class SkillLevel(models.Model):
    skills = models.ManyToManyField(Skill, related_name="levels")
    level = models.CharField(
        max_length=1,
        choices=(("1", "Chill"), ("2", "Medium"), ("3", "Challenge")),
        default=1,
    )
    description = models.CharField(max_length=200)
    example_task = models.ForeignKey(Task, default=None, null=True, on_delete=models.SET_DEFAULT)
    tasks = models.ManyToManyField(Task, related_name="skill_levels")
    generators = models.ManyToManyField(TaskGenerator, related_name="skill_levels")
    required_passes = models.IntegerField(default=1)

    def get_add_skill_to_skill_level_url(self):
        return f"/topic/{self.skills.all()[0].topic.pk}/skill_level/{self.pk}/add_skill_to_skill_level"

    def get_edit_url(self):
        return f"/topic/{self.skills.all()[0].topic.pk}/skill_level/{self.pk}/edit"

    def get_delete_url(self):
        return f"/topic/{self.skills.all()[0].topic.pk}/skill_level/{self.pk}/delete"

    def get_add_task_url(self):
        return f"/topic/{self.skills.all()[0].topic.pk}/skill_level/{self.pk}/task/add"

    def get_add_generator_url(self):
        return f"/topic/{self.skills.all()[0].topic.pk}/skill_level/{self.pk}/generator/add"


# What happens here??
def delete_students(sender, instance, **kwargs):
    students = get_user_model().objects.filter(your_stage=None, is_staff=False)
    for student in students:
        student.delete()


post_delete.connect(delete_students, sender=Stage)
