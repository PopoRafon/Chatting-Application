from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=60, label='Email address', min_length=4, required=True)
    username = forms.CharField(max_length=40, min_length=1, label='Username', required=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']
