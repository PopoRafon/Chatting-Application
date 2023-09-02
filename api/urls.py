from django.urls import path
from rest_framework.schemas import get_schema_view
from . import views
from django.views.generic import TemplateView

schema_view = get_schema_view(
    title='OpenAPI Discord Clone',
    description='The Discord Clone API is designed to provide the necessary functionality for managing users and chat messages within a Discord-like application. This API allows you to perform operations such as retrieving user information, fetching chat messages, and managing chat rooms.',
    version='1.0.0'
)

urlpatterns = [
    path('', TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url':'openapi-schema'}
    ), name='api-home'),
    path('openapi-schema', schema_view, name='openapi-schema'),
    path('users', views.AllUsersAPIView.as_view(), name='api-users-all'),
    path('users/<id>', views.SingleUserAPIView.as_view(), name='api-users-single'),
    path('chat/<chat_id>/messages', views.AllChatMessagesAPIView.as_view(), name='api-chat-messages-all'),
    path('chat/<chat_id>/messages/<id>', views.SingleChatMessageAPIView.as_view(), name='api-chat-messages-single'),
    path('chat/<id>', views.ChatAPIView.as_view(), name='api-chat'),
]
