from django.urls import path
from rest_framework.schemas import get_schema_view
from . import views

schema_view = get_schema_view(
    title='Discord API',
    description='API',
    version='1.0.0'
)

urlpatterns = [
    path('', schema_view, name='api-schema'),
    path('users', views.AllUsersAPIView.as_view(), name='api-users-all'),
    path('users/<id>', views.SingleUserAPIView.as_view(), name='api-users-single'),
    path('chat/<chat_id>/messages', views.AllChatMessagesAPIView.as_view(), name='api-chat-messages-all'),
    path('chat/<chat_id>/messages/<id>', views.SingleChatMessageAPIView.as_view(), name='api-chat-messages-single'),
    path('chat/<id>', views.ChatAPIView.as_view(), name='api-chat')
]
