from django.test import SimpleTestCase
from django.urls import reverse, resolve
from chat import views


class TestChatUrls(SimpleTestCase):

    def test_chat_home_url_resolves(self):
        url = reverse('chat-home')

        resolver = resolve(url)

        self.assertEqual(resolver.func.view_class, views.ChatHomeView)

    def test_chat_room_url_resolves(self):
        url = reverse('chat-room', kwargs={'id': 1})

        resolver = resolve(url)

        self.assertEqual(resolver.func.view_class, views.ChatRoomView)
