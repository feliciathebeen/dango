from django.db import models
from django.contrib.auth.models import AbstractUser
from django import forms


class User(AbstractUser):
    followings = models.ManyToManyField(
        "self", related_name="followers", symmetrical=False
    )