from django.test import SimpleTestCase
from django.urls import reverse, resolve
import main.views as views


class TestHomeUrls(SimpleTestCase):

    def test_home_view_url_resolves(self):
        url = reverse('home')
        resolver = resolve(url)

        self.assertEqual(resolver.func.view_class, views.HomeView)


class TestAccountUrls(SimpleTestCase):

    def test_register_url_resolves(self):
        url = reverse('register')
        resolver = resolve(url)

        self.assertEqual(resolver.func.view_class, views.RegisterView)

    def test_login_url_resolves(self):
        url = reverse('login')
        resolver = resolve(url)

        self.assertEqual(resolver.func.view_class, views.LoginView)


class TestTermsOfServiceUrls(SimpleTestCase):

    def test_terms_of_service_url_resolves(self):
        url = reverse('terms-of-service')
        resolver = resolve(url)

        self.assertEqual(resolver.func, views.terms_of_service_view)


class TestPasswordUrls(SimpleTestCase):

    def test_password_change_url_resolves(self):
        url = reverse('password-change')
        resolver = resolve(url)

        self.assertEqual(resolver.func.view_class, views.PasswordChangeView)

    def test_password_reset_url_resolves(self):
        url = reverse('password-reset')
        resolver = resolve(url)

        self.assertEqual(resolver.func.view_class, views.PasswordResetView)

    def test_password_reset_confirm_url_resolves(self):
        url = reverse('password-reset-confirm', kwargs={'uidb64': '1', 'token': '1'})
        resolver = resolve(url)

        self.assertEqual(resolver.func.view_class, views.PasswordResetConfirmView)
