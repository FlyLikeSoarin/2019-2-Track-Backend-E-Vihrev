from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Q

class User(AbstractUser):
    avatar = models.CharField(max_length=100, null=True, blank=True)
    settings = models.CharField(max_length=1000, null=True, blank=True)

    def search_for_user(search_term):
        return User.objects.filter(username__contains=search_term).all()

    def get_by_id(id):
        return User.objects.get(id__exact=id)

    def get_by_username(username):
        try:
            return User.objects.filter(username=username)[0]
        except IndexError:
            return False

    def fix_passwords():
        for user in User.objects.all():
            if len(user.password) < 15:  # hash is a longer string
                user.set_password(user.password)
                user.save()
