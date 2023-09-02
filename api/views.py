from .serializers import UserSerializer, ChatMessageSerializer, ChatSerializer
from main.models import Profile
from chat.models import Chat, ChatMessage
from rest_framework import generics
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from .permissions import ChatMessageObjectPermissions, ChatMessageModelPermissions, ChatObjectPermissions


class AllUsersAPIView(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        return Profile.objects.all()


class SingleUserAPIView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    lookup_field = 'id'

    def get_object(self):
        id = self.kwargs['id']
        return Profile.objects.get(id=id)


class AllChatMessagesAPIView(generics.ListCreateAPIView):
    serializer_class = ChatMessageSerializer
    permission_classes = [IsAuthenticated, ChatMessageModelPermissions]

    def perform_create(self, serializer):
        chat_id = self.kwargs['chat_id']
        chat = get_object_or_404(Chat, id=chat_id)

        serializer.validated_data.update({'chat': chat})
        serializer.validated_data.update({'sender': self.request.user})

        serializer.save()

    def get_queryset(self):
        query_string = self.request.GET
        chat_id = self.kwargs['chat_id']
        messages = ChatMessage.objects.filter(chat__id=chat_id)

        if query_string:
            start = query_string.get('start')
            end = query_string.get('end')

            messages = messages[int(start):int(end)]

        return messages


class SingleChatMessageAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ChatMessageSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated, ChatMessageObjectPermissions]

    def get_queryset(self):
        return ChatMessage.objects.all()


class ChatAPIView(generics.DestroyAPIView):
    serializer_class = ChatSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated, ChatObjectPermissions]

    def get_queryset(self):
        return Chat.objects.all()
