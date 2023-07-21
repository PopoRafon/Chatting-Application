from django.test import TestCase
from main.forms import RegistrationForm, LoginForm
from django.contrib.auth.models import User


class TestRegistrationForm(TestCase):

    def test_registration_form_with_valid_data(self):
        form = RegistrationForm(data={
            'email': 'testemail@gmail.com',
            'username': 'testusername',
            'password1': 'testpassword',
            'password2': 'testpassword',
        })

        self.assertTrue(form.is_valid())

    def test_registration_form_with_no_data(self):
        form = RegistrationForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 4)


class TestLoginForm(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='test', password='testpassword')

    def test_login_form_with_valid_data(self):
        form = LoginForm(data={
            'username': 'test',
            'password': 'testpassword'
        })

        self.assertTrue(form.is_valid())

    def test_login_form_with_no_data(self):
        form = LoginForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)
