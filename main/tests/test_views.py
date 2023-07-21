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

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/home.html')
        

class TestRegisterView(TestCase):

    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')

    def test_register_view_GET(self):
        response = self.client.get(self.register_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/register.html')

    def test_register_view_GET_authenticated_user(self):
        user = User.objects.create(username='test')
    
        self.client.force_login(user)
        response = self.client.get(self.register_url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

    def test_register_view_POST_authenticated_user(self):
        user = User.objects.create(username='user')

        self.client.force_login(user)
        response = self.client.post(self.register_url, data={})

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

    def test_register_view_POST_invalid_data(self):
        response = self.client.post(self.register_url, data={})

        self.assertEqual(response.status_code, 422)
        self.assertEqual(User.objects.count(), 0)

    def test_register_view_POST_create_new_user(self):
        response = self.client.post(self.register_url, data={
            'email': 'testemail@gmail.com',
            'username': 'testusername',
            'password1': 'testpassword',
            'password2': 'testpassword',
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.count(), 1)
        self.assertRedirects(response, reverse('home'))


class TestLoginView(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='test', password='testpassword')
        self.login_url = reverse('login')

    def test_login_view_GET(self):
        response = self.client.get(self.login_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/login.html')

    def test_login_view_GET_authenticated_user(self):
        self.client.force_login(self.user)
        response = self.client.get(self.login_url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

    def test_login_view_POST_login_user_to_account(self):
        response = self.client.post(self.login_url, data={
            'username': 'test',
            'password': 'testpassword'
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(int(self.client.session['_auth_user_id']), self.user.pk)
        self.assertRedirects(response, reverse('home'))

    def test_login_view_POST_invalid_data(self):
        response = self.client.post(self.login_url, data={})

        self.assertEqual(response.status_code, 422)
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_login_view_POST_authenticated_user(self):
        self.client.force_login(self.user)
        response = self.client.post(self.login_url, data={})

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))
