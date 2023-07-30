from django.urls import path
from . import views

urlpatterns = [
    path('@me', views.ChatHomeView.as_view(), name='chat-home'),
    path('@me/<id>', views.ChatRoomView.as_view(), name='chat-room'),
]
