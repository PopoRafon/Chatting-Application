from django.urls import path
from . import views

urlpatterns = [
    path('@me', views.ChatHomeView.as_view(), name='chat-home'),
    path('@me/<room_name>', views.ChatRoomView.as_view(), name='chat-room')
]
