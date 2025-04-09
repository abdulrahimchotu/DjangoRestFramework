from django.contrib.auth.hashers import make_password
from django.db import models

class UserManager(models.Manager):
    def create(self, **kwargs):
        if 'password' in kwargs:
            kwargs['password'] = make_password(kwargs['password'])
        return super().create(**kwargs)