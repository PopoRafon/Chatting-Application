from datetime import timedelta
from django.contrib.auth.models import User
from django.db import models


class Chat(models.Model):
    users = models.ManyToManyField(User, related_name='chats')


class ChatMessage(models.Model):
    chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='chat_messages', on_delete=models.CASCADE)
    body = models.TextField(max_length=512)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def was_modified(self):
        threshold = timedelta(milliseconds=500)
        return abs(self.modified - self.created) > threshold

    class Meta:
        ordering = ['-created']


class Request(models.Model):
    sender = models.ForeignKey(User, related_name='sended_requests', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_requests', on_delete=models.CASCADE)
    content = models.CharField(max_length=255, default='Do you want to create new chat?')
    sended = models.DateTimeField(auto_now_add=True)
