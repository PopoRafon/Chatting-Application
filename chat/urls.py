from django.urls import path
from . import views

urlpatterns = [
    path('@me', views.ChatHomeView.as_view(), name='chat-home'),
    path('@me/<str:id>', views.ChatRoomView.as_view(), name='chat-room')
]
