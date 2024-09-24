# myapp/backends.py
from django.contrib.auth.backends import BaseBackend
from .models import Client


class MyAuthBackend(BaseBackend):

    def authenticate(self, request, username=None, password=None,):
        try:
            user = Client.objects.get(username=username)
            if user.password == password:
                return user
        except Client.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Client.objects.get(pk=user_id)
        except Client.DoesNotExist:
            return None

