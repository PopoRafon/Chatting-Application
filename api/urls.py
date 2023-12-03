from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.urls import path
from rest_framework.schemas import get_schema_view
from . import views

schema_view = get_schema_view(
    title='OpenAPI Chatting Application',
    description='Chatting Application API is designed to provide the necessary functionality for managing users and chat messages.',
    version='1.0.0'
)

urlpatterns = [
    path('', login_required(TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url':'openapi-schema'},
    )), name='api-home'),
    path('openapi-schema', schema_view, name='openapi-schema'),
    path('users', views.AllUsersAPIView.as_view(), name='api-users-all'),
    path('users/<id>', views.SingleUserAPIView.as_view(), name='api-users-single'),
    path('chat/<chat_id>/messages', views.AllChatMessagesAPIView.as_view(), name='api-chat-messages-all'),
    path('chat/<chat_id>/messages/<message_id>', views.SingleChatMessageAPIView.as_view(), name='api-chat-messages-single'),
    path('chat/<id>', views.ChatAPIView.as_view(), name='api-chat'),
    path('requests', views.RequestAPIView.as_view(), name='api-request'),
    path('requests/<id>', views.RequestDecisionAPIView.as_view(), name='api-request-decision')
]
