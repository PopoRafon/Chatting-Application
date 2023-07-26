from typing import Any, Dict
from django.views.generic import TemplateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Chat
from django.urls import reverse_lazy


class ChatHomeView(LoginRequiredMixin, TemplateView):
    template_name = 'chat/chat_components/chat_home.html'
    redirect_field_name = None


class ChatRoomView(LoginRequiredMixin, DetailView):
    model = Chat
    pk_url_kwarg = 'id'
    template_name = 'chat/chat_components/chat_room.html'
    redirect_field_name = None

    def get_queryset(self):
        query_set = super().get_queryset()
        return query_set.prefetch_related('users', 'messages')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        users = context['chat'].users
        context['id'] = self.kwargs['id']
        context['opposite_user'] = users.first() if users.first() != self.request.user else users.last()
        return context
