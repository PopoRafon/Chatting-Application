from rest_framework.test import APISimpleTestCase
from api import views
from django.urls import reverse, resolve


class TestUserUrls(APISimpleTestCase):

    def test_all_users_url_resolves(self):
        url = reverse('api-users-all')

        resolver = resolve(url)

        self.assertEqual(resolver.func.view_class, views.AllUsersAPIView)

    def test_single_user_url_resolves(self):
        url = reverse('api-users-single', kwargs={'id': 1})

        resolver = resolve(url)

        self.assertEqual(resolver.func.view_class, views.SingleUserAPIView)


class TestChatMessageUrls(APISimpleTestCase):

    def test_all_chat_messages_url_resolves(self):
        url = reverse('api-chat-messages-all', kwargs={'chat_id': 1})

        resolver = resolve(url)

        self.assertEqual(resolver.func.view_class, views.AllChatMessagesAPIView)

    def test_single_chat_message_url_resolves(self):
        url = reverse('api-chat-messages-single', kwargs={'chat_id': 1, 'id': 1})

        resolver = resolve(url)

        self.assertEqual(resolver.func.view_class, views.SingleChatMessageAPIView)


class TestChatUrls(APISimpleTestCase):

    def test_chat_url_resolves(self):
        url = reverse('api-chat', kwargs={'id': 1})

        resolver = resolve(url)

        self.assertEqual(resolver.func.view_class, views.ChatAPIView)


class TestRequestUrls(APISimpleTestCase):

    def test_request_url_resolves(self):
        url = reverse('api-request')
    
        resolver = resolve(url)

        self.assertEqual(resolver.func.view_class, views.RequestAPIView)

    def test_request_decision_url_resolves(self):
        url = reverse('api-request-decision', kwargs={'id': 1})

        resolver = resolve(url)

        self.assertEqual(resolver.func.view_class, views.RequestDecisionAPIView)
