from django.contrib.auth.models import User
from django.db import models

from exam.models import Test, StudentTest
from topic.models import SkillLevel

MARK_CHOICES = (("tick", "✓"), ("cross", "☓"), ("G", "G"), ("B", "B"), ("nb", "nb"))
TYPE_CHOICES = (("T", "Test"), ("C", "Conversation"), ("O", "Observation"))


class Grade(models.Model):
    student = models.ForeignKey(User, default=1, on_delete=models.SET_DEFAULT)
    skill_level = models.ForeignKey(SkillLevel, default=1, on_delete=models.SET_DEFAULT)
    value = models.CharField(max_length=5, choices=MARK_CHOICES, default="nb")
    type = models.CharField(
        max_length=1,
        choices=TYPE_CHOICES,
        default=1,
    )
    comment = models.CharField(max_length=200)
    publish_date = models.DateTimeField(auto_now_add=True)
    test = models.ForeignKey(Test, null=True, on_delete=models.SET_NULL)
    student_test = models.ForeignKey(StudentTest, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.value}, poziom {self.skill_level.level}, typ {self.type} " \
               f"dzień {self.publish_date.strftime('%d-%m-%Y')}"
