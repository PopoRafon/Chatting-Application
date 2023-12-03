from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('terms-of-service/', views.TermsOfServiceView.as_view(), name='terms-of-service'),
    path('password/change', views.PasswordChangeView.as_view(), name='password-change'),
    path('password/reset', views.PasswordResetView.as_view(), name='password-reset'),
    path('password/reset/<uidb64>/<token>', views.PasswordResetConfirmView.as_view(), name='password-reset-confirm')
]
