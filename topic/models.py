from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.db.models.signals import pre_save, post_delete
from django.contrib.auth import get_user_model, get_user
from django.db.models.fields.related import RelatedField

User = settings.AUTH_USER_MODEL

# Create your models here.
    

class Stage(models.Model):
    title   = models.CharField(max_length=20)
    teacher = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    number  = models.IntegerField(null=True, blank=True)
    passwords = models.QuerySet()
    def __str__(self):
        return self.title
    
    def get_update_url(self):
        return f"/your_classes/add/next/{self.pk}"
    
    def get_passwords_url(self):
        return f"/your_classes/{self.pk}/passwords/"
    

class Your_Stage(models.Model):
    user  = models.OneToOneField(User, on_delete=models.CASCADE)
    role  = models.CharField(max_length=8, choices=[('STUDENT', 'Student'), ('TEACHER', 'Teacher')], default='STUDENT')
    stage = models.ForeignKey(Stage, null=True, blank=True, on_delete=models.CASCADE)





class Topic(models.Model):
    title   = models.CharField(max_length=120)
    slug    = models.SlugField(unique = True)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    stage   = models.ForeignKey(Stage, on_delete=models.CASCADE)
    def get_absolute_url(self):
        return f"/topic/{self.slug}"
    
    def get_update_url(self):
        return f"/topic/{self.slug}/edit/"
    
    def get_add_skill_url(self):
        return f"/topic/{self.slug}/add/"
    
    def get_delete_url(self):
        return f"/topic/{self.slug}/delete/"
    
    def __str__(self):
        return self.title

class Skill(models.Model):
    title       = models.CharField(max_length=120)
    slug        = models.SlugField(unique = True)
    topic       = models.ForeignKey(Topic, default = 1, on_delete = models.CASCADE)

    def get_absolute_url(self):
        return f"/topic/{self.topic.slug}/skill/{self.slug}"
    
    def get_edit_url(self):
        return f"/topic/{self.topic.slug}/skill/{self.slug}/edit"
    
    def get_delete_url(self):
        return f"/topic/{self.topic.slug}/skill/{self.slug}/delete"
    
    def __str__(self):
        return self.title
    

class Grade(models.Model):
    CHOICES = (
        ("tick", "✓"),
        ("cross", "☓"),
        ("G", "G"),
        ("B", "B"),
        ("nb", "nb")
    )
    student = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    skill   = models.ForeignKey(Skill, default=1, on_delete=models.CASCADE)
    value   = models.CharField(max_length=5, choices=CHOICES, default="nb")
    level   = models.CharField(max_length=1, choices=(('1','Chill'), ('2','Medium'), ('3', 'Challenge')), default=1)



User = get_user_model()
def delete_students(sender, instance, **kwargs):
    students = User.objects.filter(your_stage=None, is_staff=False)
    for student in students:
        student.delete()

post_delete.connect(delete_students, sender=Stage)