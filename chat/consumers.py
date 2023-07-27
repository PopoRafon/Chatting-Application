import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Chat, ChatMessage
from main.models import Profile
from channels.db import database_sync_to_async
from django.core.serializers.json import DjangoJSONEncoder


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        user = self.scope['user']

        message = text_data_json['message']

        if len(message) >= 512 or len(message.replace(' ', '').replace('\n', '')) == 0: return

        chat = await database_sync_to_async(Chat.objects.get)(id=self.room_name)

        message = await database_sync_to_async(ChatMessage.objects.create)(chat=chat, sender=user, body=message)

        await self.channel_layer.group_send(self.room_group_name, {
            'type': 'chat_message',
            'user': user,
            'message': message
        })

    async def chat_message(self, event):
        message = event['message']
        user = event['user']
        profile = await database_sync_to_async(Profile.objects.get)(user=user)

        await self.send(json.dumps({
            'message': message.body,
            'sender': user.username,
            'avatar': profile.avatar.url,
            'created': {'hour': f'{message.created.hour:02d}', 'minute': f'{message.created.minute:02d}'}
        }, cls=DjangoJSONEncoder))
