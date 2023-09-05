from django.test import TestCase
from chat.models import Chat, ChatMessage
from django.contrib.auth.models import User


class TestChatModels(TestCase):

    def setUp(self):
        self.first_user = User.objects.create(username='first_user')
        self.second_user = User.objects.create(username='second_user')
        self.chat = Chat.objects.create()
        self.chat.users.set((self.first_user, self.second_user))

    def test_chat_users_are_set_correctly(self):
        self.assertEqual(self.chat.users.count(), 2)

    def test_chat_message_is_added_correctly(self):
        ChatMessage.objects.create(sender=self.first_user, chat=self.chat, body='test body')

        self.assertEqual(self.chat.messages.count(), 1)
        self.assertEqual(self.chat.messages.first().sender, self.first_user)
        self.assertEqual(self.chat.messages.first().body, 'test body')
