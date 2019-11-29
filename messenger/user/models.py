from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Q

class User(AbstractUser):
    username = models.CharField(max_length=32, null=False, unique=True)
    password = models.IntegerField(null=False)
    email_address = models.EmailField(null=False)
    avatar = models.CharField(max_length=100, null=True)
    settings = models.CharField(max_length=1000, null=True)

    def search_for_user(search_term):
        return User.objects.filter(username__contains=search_term).all()

    def get_by_id(id):
        return User.objects.get(id__exact=id)
