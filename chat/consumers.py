import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Chat, ChatMessage
from main.models import Profile
from channels.db import database_sync_to_async
from .permissions import has_chat_access


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            self.chat_name = self.scope['url_route']['kwargs']['chat_name']
            self.chat_group_name = f'chat_{self.chat_name}'

            if not await has_chat_access(self.scope['user'], self.chat_name):
                await self.close()
            else:
                await self.channel_layer.group_add(self.chat_group_name, self.channel_name)

                await self.accept()
        except Exception:
            await self.close()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.chat_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        
        if len(message) >= 512 or len(message.replace(' ', '').replace('\n', '')) == 0: return

        user = self.scope['user']
        profile = await database_sync_to_async(Profile.objects.get)(user=user)

        chat = await database_sync_to_async(Chat.objects.get)(id=self.chat_name)

        message = await database_sync_to_async(ChatMessage.objects.create)(chat=chat, sender=user, body=message)

        await self.channel_layer.group_send(self.chat_group_name, {
            'type': 'chat_message',
            'alias': profile.alias,
            'body': message.body,
            'avatar': profile.avatar.url,
            'created': f'{message.created.strftime("%Y-%m-%d %H:%M")}'
        })

    async def chat_message(self, event):
        body = event['body']
        user = event['alias']
        avatar = event['avatar']
        created = event['created']

        await self.send(json.dumps({
            'body': body,
            'sender': user,
            'avatar': avatar,
            'created': created
        }))
