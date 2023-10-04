from django.contrib.auth.models import User
from django.db import models

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

    def __str__(self):
        return f"{self.value} for {self.skill_level.level} based on {self.type} " \
               f"at {self.publish_date.strftime('%d-%m-%Y')}"
