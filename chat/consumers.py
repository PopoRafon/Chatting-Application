import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from main.models import Profile
from .models import Chat, ChatMessage


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            self.chat_name = self.scope['url_route']['kwargs']['chat_name']
            self.chat_group_name = f'chat_{self.chat_name}'
            self.user = self.scope['user']
            self.chat = await database_sync_to_async(Chat.objects.prefetch_related('users').get)(id=self.chat_name)

            if self.user in self.chat.users.all():
                await self.channel_layer.group_add(self.chat_group_name, self.channel_name)

                await self.accept()
            else:
                await self.close()
        except Exception:
            await self.close()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.chat_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action_type = text_data_json['type']

        match action_type:
            case 'send_message':
                await self.create_message(text_data_json)
            case 'delete_message':
                await self.delete_message(text_data_json)
            case 'modify_message':
                await self.modify_message(text_data_json)
            case _:
                await self.send_error()

    async def create_message(self, data):
        received_message = data['message']

        if await self.validate_message_content(received_message):
            profile = await database_sync_to_async(Profile.objects.get)(user=self.user)

            message = await database_sync_to_async(ChatMessage.objects.create)(chat=self.chat, sender=self.user, body=received_message)

            await self.channel_layer.group_send(self.chat_group_name, {
                'type': 'send_created_message',
                'id': message.id,
                'sender': profile.alias,
                'body': message.body,
                'avatar': profile.avatar.url,
                'created': message.created.strftime("%Y-%m-%d %H:%M")
            })
        else:
            await self.send_error()

    async def delete_message(self, data):
        message_id = data['message_id']

        message = await database_sync_to_async(ChatMessage.objects.get)(id=message_id, sender=self.user)

        await message.adelete()

        await self.channel_layer.group_send(self.chat_group_name, {
            'type': 'send_deleted_message',
            'id': message_id
        })
        
    async def modify_message(self, data):
        message_id = data['message_id']
        body = data['body']

        if await self.validate_message_content(body):
            message = await database_sync_to_async(ChatMessage.objects.prefetch_related('sender').get)(id=message_id)

            if message.sender == self.user:
                message.body = body

                await message.asave()

                await self.channel_layer.group_send(self.chat_group_name, {
                    'type': 'send_modified_message',
                    'id': message_id,
                    'time': message.modified.strftime("%H:%M"),
                    'body': body
                })
            else:
                await self.send_error()
        else:
            await self.send_error()

    async def send_error(self):
        await self.send(json.dumps({
            'type': 'error',
            'message': 'Error occurred when trying to process your request.'
        }))

    async def send_created_message(self, event):
        _, id, sender, body, avatar, created = event.values()

        await self.send(json.dumps({
            'type': 'message_created',
            'id': id,
            'sender': sender,
            'body': body,
            'avatar': avatar,
            'created': created
        }))

    async def send_deleted_message(self, event):
        id = event['id']

        await self.send(json.dumps({
            'type': 'message_deleted',
            'id': id
        }))

    async def send_modified_message(self, event):
        _, id, time, body = event.values()

        await self.send(json.dumps({
            'type': 'message_modified',
            'id': id,
            'time': time,
            'body': body
        }))

    async def validate_message_content(self, message):
        """
        Method validates received message content.
        Returns True if all validations pass otherwise returns False.
        """
        if len(message) >= 511: return False
        if len(message.replace(' ', '').replace('\n', '')) == 0: return False

        return True
