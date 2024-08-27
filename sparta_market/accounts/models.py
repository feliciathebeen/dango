from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    user_id = models.CharField(max_length=10, default='default_id')
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    following = models.ManyToManyField(
    "self", symmetrical=False, related_name="followers"
)
