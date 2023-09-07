from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=60, min_length=8, label='Email address', required=True)
    username = forms.CharField(max_length=16, min_length=4, label='Username', required=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    password = forms.CharField(max_length=60, label='Password', widget=forms.PasswordInput(), required=True)
    username = forms.CharField(max_length=16, min_length=4, label='Username', required=True)
