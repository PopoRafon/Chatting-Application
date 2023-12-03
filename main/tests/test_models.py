from django.contrib.auth.models import User
from django.test import TestCase
from main.models import Profile


class TestUserModels(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='test')

    def test_profile_is_created_when_user_gets_created(self):
        self.assertEqual(Profile.objects.count(), 1)
        self.assertEqual(Profile.objects.first().user, self.user)
