from django.db import models


class Task(models.Model):
    content = models.CharField(max_length=500, default="")
    source = models.CharField(max_length=100, default="")
    topic = models.ForeignKey("topic.Topic", on_delete=models.PROTECT)

    def get_edit_url(self):
        return f"/topic/{self.topic.pk}/task/{self.pk}/edit"

    def get_delete_url(self):
        return f"/topic/{self.topic.pk}/task/{self.pk}/delete"


class TaskGenerator(models.Model):
    code = models.CharField(max_length=1000)
    topic = models.ForeignKey("topic.Topic", on_delete=models.PROTECT)

    def get_edit_url(self):
        return f"/topic/{self.topic.pk}/generator/{self.pk}/edit"

    def get_delete_url(self):
        return f"/topic/{self.topic.pk}/generator/{self.pk}/delete"
