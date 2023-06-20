from django.db import models

# Create your models here.


class GitLab(models.Model):
    chat_id = models.TextField(unique=True)
    json = models.JSONField()
    project_id = models.IntegerField(default=0)
    token = models.CharField(max_length=255, null=True)
    url = models.CharField(max_length=255, null=True)