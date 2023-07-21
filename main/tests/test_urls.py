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
