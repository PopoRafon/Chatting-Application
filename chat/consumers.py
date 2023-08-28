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
                self.chat_instance = await database_sync_to_async(Chat.objects.get)(id=self.chat_name)

                await self.channel_layer.group_add(self.chat_group_name, self.channel_name)

                await self.accept()
        except Exception:
            await self.close()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.chat_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action_type = text_data_json['type']
        user = self.scope['user']

        if action_type == 'send_message':
            await self.create_message(user, text_data_json['message'])
        elif action_type == 'delete_message':
            await self.delete_message(user, text_data_json['message_id'])
        elif action_type == 'modify_message':
            await self.modify_message(user, text_data_json['message_id'], text_data_json['body'])
        else:
            await self.channel_layer.group_send(self.chat_group_name, {
                'type': 'send_error'
            })

    async def send_error(self, event):
        await self.send(json.dumps({
            'error': 'Provided action type is not supported.'
        }))

    async def send_created_message(self, event):
        id = event['id']
        sender = event['sender']
        body = event['body']
        avatar = event['avatar']
        created = event['created']

        await self.send(json.dumps({
            'message_created': 'Message was successfuly created.',
            'id': id,
            'sender': sender,
            'body': body,
            'avatar': avatar,
            'created': created
        }))

    async def send_deleted_message(self, event):
        id = event['id']

        await self.send(json.dumps({
            'message_deleted': 'Message was successfuly deleted.',
            'id': id
        }))

    async def send_modified_message(self, event):
        id = event['id']
        time = event['time']
        body = event['body']

        await self.send(json.dumps({
            'message_modified': 'Message was successfuly modified.',
            'id': id,
            'time': time,
            'body': body
        }))

    async def create_message(self, user, received_message):
        try:
            if len(received_message) >= 511 or len(received_message.replace(' ', '').replace('\n', '')) == 0: return

            profile = await database_sync_to_async(Profile.objects.get)(user=user)

            message = await database_sync_to_async(ChatMessage.objects.create)(chat=self.chat_instance, sender=user, body=received_message)

            await self.channel_layer.group_send(self.chat_group_name, {
                'type': 'send_created_message',
                'id': message.id,
                'sender': profile.alias,
                'body': message.body,
                'avatar': profile.avatar.url,
                'created': message.created.strftime("%Y-%m-%d %H:%M")
            })
        except Exception:
            return

    async def delete_message(self, user, message_id):
        try:
            message = await database_sync_to_async(ChatMessage.objects.get)(id=message_id, sender=user)

            await message.adelete()

            await self.channel_layer.group_send(self.chat_group_name, {
                'type': 'send_deleted_message',
                'id': message_id
            })
        except Exception:
            return
        
    async def modify_message(self, user, message_id, body):
        try:
            if len(body) >= 511 or len(body.replace(' ', '').replace('\n', '')) == 0: return

            message = await database_sync_to_async(ChatMessage.objects.get)(id=message_id, sender=user)

            message.body = body

            await message.asave()

            await self.channel_layer.group_send(self.chat_group_name, {
                'type': 'send_modified_message',
                'id': message_id,
                'time': message.modified.strftime("%H:%M"),
                'body': body
            })
        except Exception:
            return
