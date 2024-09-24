from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django import forms

from browser.models import Estate


class ClientManager(BaseUserManager):
    def create_user(self, username, password=None):
        user = self.model(username=username)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password):
        user = self.create_user(username, password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class Client (AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=5, unique=True)
    password = models.CharField(max_length=11, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    applications = models.ManyToManyField(Estate, related_name="applications")
    # classes = models.CharField(max_length=255)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['password']

    objects = ClientManager()

    def __str__(self):
        return self.username