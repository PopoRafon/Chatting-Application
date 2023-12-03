from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from chat.models import Chat


class TestChatViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username='test')
        self.chat = Chat.objects.create()
        self.chat_home_url = reverse('chat-home')
        self.chat_room_url = reverse('chat-room', kwargs={'id': self.chat.id})

    def test_chat_home_view_GET(self):
        response = self.client.get(self.chat_home_url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

    def test_chat_home_view_GET_authenticated_user(self):
        self.client.force_login(self.user)
        response = self.client.get(self.chat_home_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chat/chat_components/home.html')

    def test_chat_room_view_GET(self):
        response = self.client.get(self.chat_room_url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

    def test_chat_room_view_GET_authenticated_user(self):
        self.client.force_login(self.user)
        response = self.client.get(self.chat_room_url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.chat_home_url)

    def test_chat_room_view_GET_user_in_chat_users(self):
        self.chat.users.add(self.user)

        self.client.force_login(self.user)
        response = self.client.get(self.chat_room_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chat/chat_components/chat_room.html')
