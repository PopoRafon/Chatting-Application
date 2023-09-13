from django.test import TestCase
from django.test.client import Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core import mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes


class TestHomeViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.home_url = reverse('home')

    def test_home_view_GET(self):
        response = self.client.get(self.home_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/home/home.html')
        

class TestRegisterView(TestCase):

    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')

    def test_register_view_GET(self):
        response = self.client.get(self.register_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/account/register.html')

    def test_register_view_GET_authenticated_user(self):
        user = User.objects.create(username='test')
    
        self.client.force_login(user)

        response = self.client.get(self.register_url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('chat-home'))

    def test_register_view_POST_authenticated_user(self):
        user = User.objects.create(username='user')

        self.client.force_login(user)

        response = self.client.post(self.register_url, data={})

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('chat-home'))

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
        self.assertRedirects(response, reverse('chat-home'))


class TestLoginView(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='test', password='testpassword')
        self.login_url = reverse('login')

    def test_login_view_GET(self):
        response = self.client.get(self.login_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/account/login.html')

    def test_login_view_GET_authenticated_user(self):
        self.client.force_login(self.user)

        response = self.client.get(self.login_url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('chat-home'))

    def test_login_view_POST_login_user_to_account(self):
        response = self.client.post(self.login_url, data={
            'username': 'test',
            'password': 'testpassword'
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(int(self.client.session['_auth_user_id']), self.user.pk)
        self.assertRedirects(response, reverse('chat-home'))

    def test_login_view_POST_invalid_data(self):
        response = self.client.post(self.login_url, data={})

        self.assertEqual(response.status_code, 422)
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_login_view_POST_authenticated_user(self):
        self.client.force_login(self.user)

        response = self.client.post(self.login_url, data={})

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('chat-home'))

    def test_logout_view_GET_authenticated_user(self):
        self.client.force_login(self.user)

        logout_url = reverse('logout')

        response = self.client.get(logout_url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))
        self.assertTrue(self.client.session.is_empty())


class TestPasswordViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(email='test@gmail.com', username='test', password='testpassword')
        self.password_change_url = reverse('password-change')
        self.password_reset_url = reverse('password-reset')
        self.uidb64 = urlsafe_base64_encode(force_bytes(self.user.id))
        self.token = default_token_generator.make_token(self.user)
        self.password_reset_confirm_url = reverse('password-reset-confirm', kwargs={'uidb64': self.uidb64, 'token': self.token})
        self.set_password_url = f'/password/reset/{self.uidb64}/set-password'

    def test_password_change_view_GET_authenticated_user(self):
        self.client.force_login(self.user)

        response = self.client.get(self.password_change_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/password/password_change.html')

    def test_password_change_view_POST_invalid_password(self):
        self.client.force_login(self.user)

        response = self.client.post(self.password_change_url, data={
            'old_password': 'testpassword',
            'new_password1': '',
            'new_password2': ''
        })

        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.get(username=self.user.username).check_password('testpassword'))

    def test_password_change_view_POST_new_password(self):
        self.client.force_login(self.user)

        response = self.client.post(self.password_change_url, data={
            'old_password': 'testpassword',
            'new_password1': 'newtestpassword',
            'new_password2': 'newtestpassword'
        })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('chat-home'))
        self.assertTrue(User.objects.get(username=self.user.username).check_password('newtestpassword'))

    def test_password_reset_view_GET(self):
        response = self.client.get(self.password_reset_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/password/password_reset.html')

    def test_password_reset_view_POST_invalid_email(self):
        response = self.client.post(self.password_reset_url, data={
            'email': 'invalid@gmail.com'
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 0)

    def test_password_reset_view_POST_email_link(self):
        response = self.client.post(self.password_reset_url, data={
            'email': 'test@gmail.com'
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to[0], 'test@gmail.com')

    def test_password_reset_confirm_view_GET(self):
        response = self.client.get(self.password_reset_confirm_url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.set_password_url)

    def test_password_reset_confirm_view_GET_set_password(self):
        response = self.client.get(self.set_password_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/password/password_reset_confirm.html')

    def test_password_reset_confirm_view_POST_invalid_data(self):
        self.client.get(self.password_reset_confirm_url)

        response = self.client.post(self.set_password_url, data={
            'new_password1': '',
            'new_password2': ''
        })

        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.get(username=self.user.username).check_password('testpassword'))

    def test_password_reset_confirm_view_POST_set_password(self):
        self.client.get(self.password_reset_confirm_url)

        response = self.client.post(self.set_password_url, data={
            'new_password1': 'newtestpassword',
            'new_password2': 'newtestpassword'
        })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(User.objects.get(username=self.user.username).check_password('newtestpassword'))
