from django.test import TestCase
from django.test.client import Client
from django.urls import reverse
from django.contrib.auth.models import User


class TestHomeViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.home_url = reverse('home')

    def test_home_view_GET(self):
        response = self.client.get(self.home_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/home.html')
        

class TestAccountViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')

    def test_register_view_GET(self):
        response = self.client.get(self.register_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/register.html')

    def test_register_view_GET_authenticated_user(self):
        user = User.objects.create(username='test')
    
        self.client.force_login(user)
        response = self.client.get(self.register_url)

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

    def test_register_view_POST_authenticated_user(self):
        user = User.objects.create(username='user')

        self.client.force_login(user)
        response = self.client.post(self.register_url, data={})

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

    def test_register_view_POST_invalid_data(self):
        response = self.client.post(self.register_url, data={})

        self.assertEquals(response.status_code, 200)
        self.assertEquals(User.objects.count(), 0)

    def test_register_view_POST_create_new_user(self):
        response = self.client.post(self.register_url, data={
            'email': 'testemail@gmail.com',
            'username': 'testusername',
            'password1': 'testpassword',
            'password2': 'testpassword',
        })

        self.assertEquals(response.status_code, 302)
        self.assertEquals(User.objects.count(), 1)
        self.assertRedirects(response, reverse('home'))
