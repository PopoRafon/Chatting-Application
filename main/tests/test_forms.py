from django.test import SimpleTestCase, TestCase
from main.forms import RegistrationForm


class TestAccountForms(TestCase):

    def test_registration_form_with_valid_data(self):
        form = RegistrationForm(data={
            'email': 'testemail@gmail.com',
            'username': 'testusername',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'checkbox': True
        })

        self.assertTrue(form.is_valid())

    def test_registration_form_with_no_data(self):
        form = RegistrationForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 5)
