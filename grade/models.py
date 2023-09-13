from django.contrib.auth.models import User
from django.db import models

from topic.models import SkillLevel


class Grade(models.Model):
    CHOICES = (("tick", "✓"), ("cross", "☓"), ("G", "G"), ("B", "B"), ("nb", "nb"))
    student = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    skill_level = models.ForeignKey(SkillLevel, default=1, on_delete=models.CASCADE)
    value = models.CharField(max_length=5, choices=CHOICES, default="nb")
    type = models.CharField(
        max_length=1,
        choices=(("T", "Test"), ("C", "Conversation"), ("O", "Observation")),
        default=1,
    )
    comment = models.CharField(max_length=200)
    publish_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.value} for {self.skill_level.level} based on {self.type} " \
               f"at {self.publish_date.strftime('%d-%m-%Y')}"
