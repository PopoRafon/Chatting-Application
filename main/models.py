from django.db import models
from django.contrib.auth.models import User
from .utils import create_avatar_name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    alias = models.CharField(max_length=16, blank=True)
    avatar = models.ImageField(null=True, default='avatar.png', upload_to=create_avatar_name)
    description = models.CharField(blank=True, max_length=200)

    def __str__(self):
        return f"User: {self.user.username}"
