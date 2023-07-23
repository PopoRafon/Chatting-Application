from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


class ChatView(LoginRequiredMixin, TemplateView):
    template_name = 'chat/chat.html'
    redirect_field_name = None
    login_url = reverse_lazy('login')
