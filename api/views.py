from .serializers import UserSerializer, GetChatMessageSerializer
from main.models import Profile
from chat.models import Chat
from rest_framework import generics
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse


@api_view(['GET'])
def HomeAPIView(request):
    endpoints = [
        'GET /api/v1/users',
        'GET /api/v1/messages/chat/<id>',
        'DELETE /api/v1/chat/<id>'
    ]
    return Response(endpoints)


class UserAPIView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = UserSerializer


class GetChatMessageAPIView(generics.ListAPIView):
    serializer_class = GetChatMessageSerializer

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
        
class DeleteChatAPIView(generics.DestroyAPIView):
    def delete(self, request, *args, **kwargs):
        try:
            user = request.user
            id = kwargs['id']
            chat = Chat.objects.get(id=id)

            if chat.users.contains(user):
                chat.delete()

                return JsonResponse({'success': 'Chat was deleted successfuly.'})
            else:
                return JsonResponse({'error': 'You are not allowed to delete this chat.'}, status=401)
        except Exception:
            return JsonResponse({'error': 'Something went wrong.'}, status=400)
