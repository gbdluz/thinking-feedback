from django.db import models


class Task(models.Model):
    content = models.CharField(max_length=500, default="")
    source = models.CharField(max_length=100, default="")


class TaskGenerator(models.Model):
    code = models.CharField(max_length=1000)
