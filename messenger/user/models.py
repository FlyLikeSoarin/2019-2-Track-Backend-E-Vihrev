from django.db import models

class User(models.Model):
    username = models.CharField(max_length=32, null=False)
    password = models.IntegerField(null=False)
    email_address = models.EmailField(null=False)
    avatar = models.CharField(max_length=100, null=True)
    settings = models.CharField(max_length=1000, null=True)
