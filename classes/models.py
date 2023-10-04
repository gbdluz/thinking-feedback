from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Stage(models.Model):
    """
    Stage is a name for a Class, but lower-letter class is python keyword,
    thus for now Class is named Stage with all the consequences.
    """
    title = models.CharField(max_length=20)
    teacher = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    number = models.IntegerField(null=True, blank=True)
    students = models.ManyToManyField(User, related_name="classes")

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
