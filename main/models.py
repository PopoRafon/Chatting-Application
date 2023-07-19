from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(null=True, default='Avatar.png')
    description = models.CharField(blank=True, max_length=200)

    def __str__(self):
        return f"User: {self.user.username}"
