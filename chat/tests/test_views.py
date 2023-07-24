from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User


class TestChatViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.chat_url = reverse('chat-home')

    def test_chat_view_GET(self):
        response = self.client.get(self.chat_url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

    def test_chat_view_GET_authenticated_user(self):
        user = User.objects.create(username='test')

        self.client.force_login(user)
        response = self.client.get(self.chat_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'chat/chat_home.html')
