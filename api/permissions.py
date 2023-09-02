from rest_framework import permissions
from chat.models import Chat
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import Http404


class ChatMessageObjectPermissions(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.method == permissions.SAFE_METHODS and obj.chat.users.contains(request.user):
            return True

        if request.user == obj.sender:
            return True

        return False


class ChatMessageModelPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        try:
            if not 'chat_id' in view.kwargs:
                return True
            
            id = view.kwargs['chat_id']
            chat = Chat.objects.get(id=id)

            if chat.users.contains(request.user):
                return True

            return False
        except ObjectDoesNotExist:
            raise Http404('Chat not found')
        

class ChatObjectPermissions(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        if obj.users.contains(request.user):
            return True

        return False
