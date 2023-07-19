from django.views.generic import TemplateView, CreateView
from django.contrib.auth.models import User
from .forms import RegistrationForm
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth import login, authenticate


class HomeView(TemplateView):
    template_name = 'main/home.html'


class RegisterView(CreateView):
    model = User
    form_class = RegistrationForm
    template_name = 'main/register.html'
    success_url = reverse_lazy('home') # Placeholder for redirect to chat application view

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        response = super().form_valid(form)
        
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)

        if user is not None:
            login(self.request, user)

        return response
