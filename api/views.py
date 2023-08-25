from .serializers import UserSerializer, ChatMessageSerializer
from main.models import Profile
from chat.models import Chat
from rest_framework import generics
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def HomeAPIView(request):
    endpoints = [
        'GET /api/v1/users',
        'GET /api/v1/messages/chat/<id>'
    ]
    return Response(endpoints)


class UserAPIView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = UserSerializer


class ChatMessageAPIView(generics.ListAPIView):
    serializer_class = ChatMessageSerializer

    def get_queryset(self):
        user = self.request.user
        id = self.kwargs['id']
        chat = get_object_or_404(Chat, id=id)

        if chat.users.contains(user):
            query_string = self.request.GET
            messages = chat.messages.all()

            if query_string:
                start = query_string.get('start')
                end = query_string.get('end')

                messages = messages[int(start):int(end)]

            return messages
        else:
            return self.permission_denied(self.request, 'You are not allowed to view this messages.')
