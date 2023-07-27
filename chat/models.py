from django.db import models
from django.contrib.auth.models import User


class Chat(models.Model):
    users = models.ManyToManyField(User, related_name='chats')


class ChatMessage(models.Model):
    chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='chat_messages', on_delete=models.CASCADE)
    body = models.TextField(max_length=512)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']


class Channel(models.Model):
    members = models.ManyToManyField(User, related_name='channels')


class ChannelMessage(models.Model):
    channel = models.ForeignKey(Channel, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='channel_messages', on_delete=models.CASCADE)
    body = models.TextField(max_length=512)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']
