from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


class ChatHomeView(LoginRequiredMixin, TemplateView):
    template_name = 'chat/chat_components/chat_home.html'
    redirect_field_name = None


class ChatRoomView(LoginRequiredMixin, TemplateView):
    template_name = 'chat/chat_components/chat_room.html'
    redirect_field_name = None
