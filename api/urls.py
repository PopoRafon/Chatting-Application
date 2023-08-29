from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeAPIView),
    path('users', views.UserAPIView.as_view()),
    path('messages/chat/<id>', views.GetChatMessageAPIView.as_view()),
    path('chat/<id>', views.DeleteChatAPIView.as_view())
]
