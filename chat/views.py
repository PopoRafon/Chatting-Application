from django.views.generic import TemplateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from .models import Chat


class ChatHomeView(LoginRequiredMixin, TemplateView):
    template_name = 'chat/chat_components/home.html'
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
        return super().get_queryset().prefetch_related('users', 'users__profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        chat_users = context['chat'].users
        
        context['user_chats'] = user.chats.prefetch_related('users', 'users__profile')
        context['id'] = self.kwargs['id']
        context['opposite_user'] = chat_users.first() if chat_users.first() != user else chat_users.last()
        context['chat_messages'] = self.get_object().messages.all().prefetch_related('sender__profile')[:25]
        
        return context
