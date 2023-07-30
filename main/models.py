from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    alias = models.CharField(max_length=80, blank=True)
    avatar = models.ImageField(null=True, default='avatar.png')
    description = models.CharField(blank=True, max_length=200)

    def __str__(self):
        return f"User: {self.user.username}"
