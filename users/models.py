from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Initial_Password(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    password = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.student.first_name} {self.student.last_name}"


class Stage(models.Model):
    title = models.CharField(max_length=20)
    teacher = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    number = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.title

    def get_update_url(self):
        return f"/your_classes/add/next/{self.pk}"

    def get_passwords_url(self):
        return f"/your_classes/{self.pk}/passwords/"

    def get_edit_url(self):
        return f"/your_classes/{self.pk}/edit"

    def get_edit_name_url(self):
        return f"/your_classes/{self.pk}/edit/name"


class Your_Stage(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(
        max_length=8,
        choices=[("STUDENT", "Student"), ("TEACHER", "Teacher")],
        default="STUDENT",
    )
    stage = models.ForeignKey(Stage, null=True, blank=True, on_delete=models.CASCADE)
