from django.test import SimpleTestCase
from django.urls import reverse, resolve
import main.views as views


class TestHomeUrls(SimpleTestCase):

    def test_home_view_url_resolves(self):
        url = reverse('home')
        resolver = resolve(url)

        self.assertEquals(resolver.func.view_class, views.HomeView)


class TestAccountUrls(SimpleTestCase):

    def test_register_url_resolves(self):
        url = reverse('register')
        resolver = resolve(url)

        self.assertEquals(resolver.func.view_class, views.RegisterView)
