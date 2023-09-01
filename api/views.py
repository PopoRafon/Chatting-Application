from .serializers import UserSerializer, ChatMessageSerializer
from main.models import Profile
from chat.models import Chat
from rest_framework import generics
from django.shortcuts import get_object_or_404
from django.http import JsonResponse


class AllUsersAPIView(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        return Profile.objects.all()


class SingleUserAPIView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    lookup_field = 'id'

    def get_object(self):
        id = self.kwargs['id']
        profile = get_object_or_404(Profile, id=id)
        return profile


class AllChatMessagesAPIView(generics.ListCreateAPIView):
    serializer_class = ChatMessageSerializer

    def post(self, request, *args, **kwargs):
        chat_id = self.kwargs['chat_id']
        chat = get_object_or_404(Chat, id=chat_id)

        if chat.users.contains(request.user):
            return super().post(request, args, kwargs)
        else:
            return self.permission_denied(request, 'You need to participate in this chat in order to create new message in this chat.')

    def perform_create(self, serializer):
        chat_id = self.kwargs['chat_id']
        chat = get_object_or_404(Chat, id=chat_id)

        serializer.validated_data.update({'chat': chat})
        serializer.validated_data.update({'sender': self.request.user})

        serializer.save()

    def get_queryset(self):
        user = self.request.user
        chat_id = self.kwargs['chat_id']
        chat = get_object_or_404(Chat, id=chat_id)

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


class SingleChatMessageAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ChatMessageSerializer
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        return self.permission_denied(request, 'Method not allowed.')

    def delete(self, request, *args, **kwargs):
        if self.check_user_permissions():
            return super().delete(request, args, kwargs)
        else:
            return self.permission_denied(request, 'You need to be message creator in order to delete this message.')

    def put(self, request, *args, **kwargs):
        if self.check_user_permissions():
            return super().put(request, args, kwargs)
        else:
            return self.permission_denied(request, 'You need to be message creator in order to edit this message.')

    def get_queryset(self):
        user = self.request.user
        chat_id = self.kwargs['chat_id']
        chat = get_object_or_404(Chat, id=chat_id)
        message = chat.messages.all()

        if chat.users.contains(user):
            return message
        else:
            return self.permission_denied(self.request, 'You need to participate in this chat in order to view this message.')

    def check_user_permissions(self):
        user = self.request.user
        creator = self.get_object().sender

        if creator == user:
            return True
        else:
            return False


class ChatAPIView(generics.DestroyAPIView):
    serializer_class = Chat

    def delete(self, request, *args, **kwargs):
        try:
            user = request.user
            id = kwargs['id']
            chat = Chat.objects.get(id=id)

            if chat.users.contains(user):
                chat.delete()

                return JsonResponse({'success': 'Chat was deleted successfuly.'})
            else:
                return JsonResponse({'error': 'You are not allowed to delete this chat.'}, status=403)
        except Exception:
            return JsonResponse({'error': 'Something went wrong.'}, status=400)
