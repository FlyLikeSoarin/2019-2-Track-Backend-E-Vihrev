from django.db import models
from user.models import User


class Chat(models.Model):
    creator = models.ForeignKey(User, models.CASCADE)
    chat_label = models.CharField(max_length=128, null=True)
    icon = models.CharField(max_length=100, null=True)


class Member(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    chat = models.ForeignKey(Chat, models.CASCADE)
    last_unseen = models.IntegerField(null=True)
