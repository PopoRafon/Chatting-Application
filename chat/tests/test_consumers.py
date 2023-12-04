import json
from django.contrib.auth.models import User
from django.test import TestCase
from channels.testing import WebsocketCommunicator
from channels.db import database_sync_to_async
from channels.routing import URLRouter
from chat.routing import websocket_urlpatterns
from chat.models import Chat, ChatMessage


class TestChatConsumer(TestCase):
    def setUp(self):
        self.first_user = User.objects.create(username='first user')
        self.second_user = User.objects.create(username='second user')
        self.chat = Chat.objects.create()
        self.chat.users.add(self.first_user)
        self.message = ChatMessage.objects.create(sender=self.first_user, chat=self.chat, body='test message')

    async def test_chat_consumer_connection_user_not_in_chat(self):
        communicator = WebsocketCommunicator(URLRouter(websocket_urlpatterns), f'ws/chat/{self.chat.id}/')
        communicator.scope['user'] = self.second_user

        connected, _ = await communicator.connect()

        self.assertFalse(connected)

        await communicator.disconnect()

    async def test_chat_consumer_create_message(self):
        communicator = WebsocketCommunicator(URLRouter(websocket_urlpatterns), f'ws/chat/{self.chat.id}/')
        communicator.scope['user'] = self.first_user

        connected, _ = await communicator.connect()

        self.assertTrue(connected)

        await communicator.send_input({
            'type': 'create_message',
            'message': 'second test message'
        })

        response = await communicator.receive_output()
        response_json = json.loads(response['text'])

        new_message = await database_sync_to_async(ChatMessage.objects.first)()
        messages_count = await database_sync_to_async(ChatMessage.objects.count)()

        self.assertTrue(response_json)
        self.assertEqual(messages_count, 2)
        self.assertEqual(response_json['type'], 'message_created')
        self.assertEqual(response_json['id'], new_message.id)
        self.assertEqual(response_json['sender'], self.first_user.username)
        self.assertEqual(response_json['body'], 'second test message')
        self.assertEqual(response_json['avatar'], self.first_user.profile.avatar.url)

        await communicator.disconnect()

    async def test_chat_consumer_delete_message(self):
        communicator = WebsocketCommunicator(URLRouter(websocket_urlpatterns), f'ws/chat/{self.chat.id}/')
        communicator.scope['user'] = self.first_user

        connected, _ = await communicator.connect()

        self.assertTrue(connected)

        await communicator.send_input({
            'type': 'delete_message',
            'message_id': self.message.id
        })

        response = await communicator.receive_output()
        response_json = json.loads(response['text'])

        messages_count = await database_sync_to_async(ChatMessage.objects.count)()

        self.assertTrue(response_json)
        self.assertEqual(messages_count, 0)
        self.assertEqual(response_json['type'], 'message_deleted')
        self.assertEqual(response_json['id'], self.message.id)

        await communicator.disconnect()

    async def test_chat_consumer_modify_message(self):
        communicator = WebsocketCommunicator(URLRouter(websocket_urlpatterns), f'ws/chat/{self.chat.id}/')
        communicator.scope['user'] = self.first_user

        connected, _ = await communicator.connect()

        self.assertTrue(connected)

        await communicator.send_input({
            'type': 'modify_message',
            'message_id': self.message.id,
            'body': 'modified message'
        })

        response = await communicator.receive_output()
        response_json = json.loads(response['text'])

        modified_message = await database_sync_to_async(ChatMessage.objects.first)()

        self.assertTrue(response_json)
        self.assertEqual(modified_message.body, 'modified message')
        self.assertEqual(response_json['body'], modified_message.body)

        await communicator.disconnect()
