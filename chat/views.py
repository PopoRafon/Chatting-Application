from django.views.generic import TemplateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Chat
from django.shortcuts import redirect
from django.http.response import JsonResponse
from django.template.loader import render_to_string
import json


class ChatHomeView(LoginRequiredMixin, TemplateView):
    template_name = 'chat/chat_components/chat_home.html'
    redirect_field_name = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user

        context['user_chats'] = user.chats.prefetch_related('users', 'users__profile')
        
        return context


class ChatRoomView(LoginRequiredMixin, DetailView):
    model = Chat
    pk_url_kwarg = 'id'
    template_name = 'chat/chat_components/chat_room.html'
    redirect_field_name = None

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and not self.get_object().users.contains(request.user):
            return redirect('chat-home')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        query_set = super().get_queryset()
        return query_set.prefetch_related('users', 'users__profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        chat_users = context['chat'].users
        
        context['user_chats'] = user.chats.prefetch_related('users', 'users__profile')
        context['id'] = self.kwargs['id']
        context['opposite_user'] = chat_users.first() if chat_users.first() != user else chat_users.last()
        context['messages'] = self.get_object().messages.all().prefetch_related('sender__profile')[:25]
        
        return context


def load_more_messages(request):
    try:
        user = request.user
        chat_id = int(request.GET.get('chat'))
        chat = Chat.objects.get(id=chat_id)
        
        if user in chat.users.all():
            length = int(request.GET.get('length'))
            new_messages = chat.messages.all()[length:length+15]
            rendered_messages = render_to_string('chat/chat_components/chat_messages.html', context={'messages': new_messages})
            return JsonResponse({'messages': rendered_messages})
        else:
            return JsonResponse({'error': 'User is not allowed to view this page.'})
    except Exception:
        return JsonResponse({'error': 'Error occured while trying to send messages.'})
