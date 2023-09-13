from django.views.generic import TemplateView, CreateView
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordResetView, PasswordResetConfirmView
from django.contrib.auth.models import User
from .forms import RegistrationForm, LoginForm
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate
from django.http.response import JsonResponse
from django.contrib import messages 


class HomeView(TemplateView):
    template_name = 'main/home/home.html'


class RegisterView(CreateView):
    model = User
    form_class = RegistrationForm
    template_name = 'main/account/register.html'
    success_url = reverse_lazy('chat-home')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('chat-home')
        return super().dispatch(request, *args, **kwargs)
    
    def form_invalid(self, form):
        return JsonResponse({'errors': form.errors}, status=422)

    def form_valid(self, form):
        response = super().form_valid(form)
        
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)

        if user is not None:
            login(self.request, user)

        return response

class LoginView(LoginView):
    form_class = LoginForm
    template_name = 'main/account/login.html'
    redirect_authenticated_user = True
    next_page = reverse_lazy('chat-home')
    
    def form_invalid(self, form):
        if form.errors.get('__all__'):
            form.errors.pop('__all__')
            form.errors['username'] = ["Credentials you provide are invalid."]
            form.errors['password'] = ["Credentials you provide are invalid."]
        return JsonResponse({'errors': form.errors}, status=422)


class LogoutView(LogoutView):
    next_page = reverse_lazy('home')


class PasswordChangeView(PasswordChangeView):
    success_url = reverse_lazy('chat-home')
    template_name = 'main/password/password_change.html'

    def form_valid(self, form):
        messages.success(self.request, 'Your password has been successfuly changed.')
        return super().form_valid(form)


class PasswordResetView(PasswordResetView):
    success_url = reverse_lazy('home')
    email_template_name = 'main/email/password_reset_email.html'
    template_name = 'main/password/password_reset.html'

    def form_valid(self, form):
        messages.success(self.request, 'Password reset link was sent to your email.')
        return super().form_valid(form)


class PasswordResetConfirmView(PasswordResetConfirmView):
    success_url = reverse_lazy('login')
    template_name = 'main/password/password_reset_confirm.html'

    def form_valid(self, form):
        messages.success(self.request, 'Your password has been successfuly changed.')
        return super().form_valid(form)


def terms_of_service_view(request):
    return render(request, 'main/terms_of_service.html')
