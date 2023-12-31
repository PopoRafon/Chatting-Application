from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView, ListCreateAPIView, CreateAPIView, DestroyAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from chat.models import Chat, ChatMessage, Request
from main.models import Profile
from .permissions import ChatMessageObjectPermissions, ChatMessageModelPermissions, ChatObjectPermissions, UserObjectPermissions
from .serializers import UserRetrieveSerializer, UserUpdateSerializer, ChatMessageSerializer, ChatSerializer, RequestSerializer


class AllUsersAPIView(ListAPIView):
    serializer_class = UserRetrieveSerializer

    def get_queryset(self):
        return Profile.objects.all().prefetch_related('user')


class SingleUserAPIView(RetrieveUpdateAPIView):
    lookup_field = 'id'
    permission_classes = [IsAuthenticated, UserObjectPermissions]
    parser_classes = [MultiPartParser]
    serializer_class = {
        'retrieve': UserRetrieveSerializer,
        'update': UserUpdateSerializer
    }

    def get_queryset(self):
        return Profile.objects.all().prefetch_related('user')

    def get_serializer_class(self):
        if self.request.method == 'PATCH' or self.request.method == 'PUT':
            return self.serializer_class.get('update')
        else:
            return self.serializer_class.get('retrieve')


class AllChatMessagesAPIView(ListCreateAPIView):
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
        messages = ChatMessage.objects.filter(chat__id=chat_id).prefetch_related('sender', 'sender__profile')

        if query_string:
            start = query_string.get('start', 0)
            end = query_string.get('end', -1)

            messages = messages[int(start):int(end)]

        return messages


class SingleChatMessageAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ChatMessageSerializer
    lookup_url_kwarg = 'message_id'
    lookup_field = 'id'
    permission_classes = [IsAuthenticated, ChatMessageObjectPermissions]

    def get_queryset(self):
        return ChatMessage.objects.all()


class ChatAPIView(DestroyAPIView):
    serializer_class = ChatSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated, ChatObjectPermissions]

    def get_queryset(self):
        return Chat.objects.all()


class RequestAPIView(CreateAPIView):
    serializer_class = RequestSerializer
    
    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            user = request.user
            id = data['receiver']
            requested_user = User.objects.get(id=id)
            check_user_sended_requests = user.sended_requests.filter(receiver=requested_user)
            check_user_received_requests = user.received_requests.filter(sender=requested_user)
            check_user_chats = Chat.objects.filter(users=user).filter(users=requested_user)

            if user == requested_user:
                return Response({'error': 'Receiver you provided is invalid.'}, status=status.HTTP_400_BAD_REQUEST)
            
            if len(check_user_sended_requests) != 0:
                return Response({'error': 'You already sended request to this user.'}, status=status.HTTP_400_BAD_REQUEST)
            
            if len(check_user_received_requests) != 0:
                return Response({'error': 'You already have request from this user in your inbox.'}, status=status.HTTP_400_BAD_REQUEST)
            
            if len(check_user_chats) != 0:
                return Response({'error': 'You already have chat with provided person.'}, status=status.HTTP_400_BAD_REQUEST)

            return super().post(request, *args, **kwargs)
        except Exception:
            return Response({'error': 'Receiver you provided is invalid.'}, status=status.HTTP_404_NOT_FOUND)

    def perform_create(self, serializer):
        user = self.request.user

        serializer.validated_data.update({'sender': user})

        serializer.save()


class RequestDecisionAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            user = request.user
            id = kwargs['id']
            request_obj = Request.objects.get(id=id)
            content = request_obj.content

            if user == request_obj.receiver:
                return Response({'content': content}, status=status.HTTP_200_OK)
            else:
                return self.permission_denied(request, 'You need to be request receiver to view this page.')
        except ObjectDoesNotExist:
            return Response({'error', 'Request you provided is invalid.'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, *args, **kwargs):
        try:
            id = kwargs['id']
            request_obj = Request.objects.get(id=id)
            data = request.data
            decision = data['decision']
            user = request.user

            if user == request_obj.receiver:
                if decision == 'accept':
                    request_obj.delete()
                    sender = request_obj.sender
                    chat = Chat.objects.create()
                    chat.users.add(user, sender)

                    return Response({'success': 'Request was successfully accepted and new chat has been created.'}, status=status.HTTP_201_CREATED)
                elif decision == 'reject':
                    request_obj.delete()

                    return Response({'success': 'Request was successfully rejected.'}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'Your response should be either accept or reject.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return self.permission_denied(request, 'You need to be request receiver to modify this request.')
        except ObjectDoesNotExist:
            return Response({'error', 'Request you provided is invalid.'}, status=status.HTTP_404_NOT_FOUND)
