from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from django.contrib.auth.models import User
from chat.models import Chat, ChatMessage


class TestUserViews(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.first_user = User.objects.create(username='first user')
        self.second_user = User.objects.create(username='second user')
        self.url = reverse('api-users-all')

    def test_all_users_view_GET(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 403)

    def test_all_users_view_GET_authenticated_user(self):
        self.client.force_login(self.first_user)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)


class TestSingleUserViews(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username='user')
        self.url = reverse('api-users-single', kwargs={'id': 1})

    def test_single_user_view_GET(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 403)

    def test_single_user_view_GET_authenticated_user(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertDictContainsSubset({'username': 'user', 'alias': 'user'}, response.data)


class TestAllChatMessagesViews(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username='first user')
        self.chat = Chat.objects.create()
        self.message = ChatMessage.objects.create(chat=self.chat, sender=self.user, body='first test message')
        self.url = reverse('api-chat-messages-all', kwargs={'chat_id': 1})
        self.post_body = {'body': 'second test message'}

    def test_all_chat_messages_GET(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 403)

    def test_all_chat_messages_GET_authenticated_user_without_chat(self):
        self.chat.delete()
        self.client.force_login(self.user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 404)

    def test_all_chat_messages_GET_authenticated_user_not_in_chat(self):
        self.client.force_login(self.user)
        
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 403)

    def test_all_chat_messages_GET_user_in_chat(self):
        self.client.force_login(self.user)
        self.chat.users.add(self.user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_all_chat_messages_GET_two_messages(self):
        self.client.force_login(self.user)
        self.chat.users.add(self.user)

        second_user = User.objects.create(username='second user')
        ChatMessage.objects.create(chat=self.chat, sender=second_user, body='second test message')

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_all_chat_messages_POST(self):
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(self.chat.messages.count(), 1)

    def test_all_chat_messages_POST_authenticated_user_not_in_chat(self):
        self.client.force_login(self.user)

        response = self.client.post(self.url, self.post_body)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(self.chat.messages.count(), 1)
    
    def test_all_chat_messages_POST_create_new_message(self):
        self.client.force_login(self.user)
        self.chat.users.add(self.user)

        response = self.client.post(self.url, self.post_body)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.chat.messages.count(), 2)
        self.assertDictContainsSubset({'sender': 'first user', 'body': 'second test message'}, response.data)


class TestSingleChatMessageViews(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username='user')
        self.chat = Chat.objects.create()
        self.message = ChatMessage.objects.create(chat=self.chat, sender=self.user, body='test message')
        self.url = reverse('api-chat-messages-single', kwargs={'id': 1, 'chat_id': 1})
        self.put_body = {'body': 'new body'}

    def test_single_chat_message_GET(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 403)

    def test_single_chat_message_GET_authenticated_user_without_chat(self):
        self.chat.delete()
        self.client.force_login(self.user)

        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 404)

    def test_single_chat_message_GET_authenticated_user_not_in_chat(self):
        self.client.force_login(self.user)

        second_user =  User.objects.create(username='second user')
        ChatMessage.objects.create(chat=self.chat, sender=second_user, body='second test message')
        second_message_url = reverse('api-chat-messages-single', kwargs={'id': 2, 'chat_id': 1})

        response = self.client.get(second_message_url)
        
        self.assertEqual(response.status_code, 403)

    def test_single_chat_message_GET_user_in_chat(self):
        self.client.force_login(self.user)
        self.chat.users.add(self.user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertDictContainsSubset({'sender': 'user', 'body': 'test message'}, response.data)

    def test_single_chat_message_DELETE(self):
        response = self.client.delete(self.url)
        
        self.assertEqual(response.status_code, 403)
        self.assertEqual(len(ChatMessage.objects.all()), 1)

    def test_single_chat_message_DELETE_authenticated_user_not_in_chat(self):
        self.client.force_login(self.user)

        second_user =  User.objects.create(username='second user')
        ChatMessage.objects.create(chat=self.chat, sender=second_user, body='second test message')
        second_message_url = reverse('api-chat-messages-single', kwargs={'id': 2, 'chat_id': 1})

        response = self.client.get(second_message_url)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(len(ChatMessage.objects.all()), 2)

    def test_single_chat_message_DELETE_user_in_chat(self):
        self.client.force_login(self.user)
        self.chat.users.add(self.user)

        second_user = User.objects.create(username='second user')
        self.chat.users.add(second_user)

        ChatMessage.objects.create(chat=self.chat, sender=second_user, body='second test message')

        second_message_url = reverse('api-chat-messages-single', kwargs={'id': 2, 'chat_id': 1})

        response = self.client.delete(second_message_url)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(len(ChatMessage.objects.all()), 2)

    def test_single_chat_message_DELETE_user_message_creator(self):
        self.client.force_login(self.user)
        self.chat.users.add(self.user)
        
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, 204)
        self.assertEqual(len(ChatMessage.objects.all()), 0)

    def test_single_chat_message_PUT(self):
        response = self.client.put(self.url, self.put_body)

        self.assertEqual(response.status_code, 403)

    def test_single_chat_message_PUT_authenticated_user_not_in_chat(self):
        self.client.force_login(self.user)

        second_user =  User.objects.create(username='second user')
        ChatMessage.objects.create(chat=self.chat, sender=second_user, body='second test message')
        second_message_url = reverse('api-chat-messages-single', kwargs={'id': 2, 'chat_id': 1})

        response = self.client.put(second_message_url, self.put_body)

        self.assertEqual(response.status_code, 403)
        self.assertNotEqual(ChatMessage.objects.get(id=2).body, self.put_body['body'])

    def test_single_chat_message_PUT_user_in_chat(self):
        self.client.force_login(self.user)
        self.chat.users.add(self.user)

        second_user = User.objects.create(username='second user')
        ChatMessage.objects.create(chat=self.chat, sender=second_user, body='second test body')
        self.chat.users.add(second_user)

        second_messsage_url = reverse('api-chat-messages-single', kwargs={'chat_id': 1, 'id': 2})
        response = self.client.put(second_messsage_url, self.put_body)

        self.assertEqual(response.status_code, 403)
        self.assertNotEqual(ChatMessage.objects.get(id=2).body, self.put_body['body'])

    def test_single_chat_message_PUT_user_message_creator(self):
        self.client.force_login(self.user)
        self.chat.users.add(self.user)

        response = self.client.put(self.url, self.put_body)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['body'], ChatMessage.objects.get(id=1).body)


class TestChatViews(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username='user')
        self.chat = Chat.objects.create()
        self.url = reverse('api-chat', kwargs={'id': 1})

    def test_chat_DELETE(self):
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(len(Chat.objects.all()), 1)

    def test_chat_DELETE_user_authenticated(self):
        self.client.force_login(self.user)

        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(len(Chat.objects.all()), 1)

    def test_chat_DELETE_user_in_chat(self):
        self.client.force_login(self.user)
        self.chat.users.add(self.user)

        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, 204)
        self.assertEqual(len(Chat.objects.all()), 0)
