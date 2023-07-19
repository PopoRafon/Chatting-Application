from django.test import TestCase
from django.contrib.auth.models import User
from main.models import Profile


class TestUserModels(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='test')

    def test_profile_is_created_when_user_gets_created(self):
        self.assertEquals(Profile.objects.count(), 1)
        self.assertEquals(Profile.objects.first().user, self.user)
