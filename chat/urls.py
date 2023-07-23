from django.urls import path
from . import views

urlpatterns = [
    path('@me', views.ChatView.as_view(), name='chat'),
]
