from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=60, label='Email address', min_length=4, required=True)
    username = forms.CharField(max_length=40, min_length=2, label='Username', required=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=40, min_length=2, label='Username', required=True)
    password = forms.CharField(max_length=60, min_length=4, label='Password', widget=forms.PasswordInput(), required=True)
