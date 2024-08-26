from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    image = models.ImageField(upload_to='images/', blank=True, default='images/default_profile_pic.png')
    following = models.ManyToManyField(
        "self", symmetrical=False, related_name="followers"
    )