from django.test import TestCase
from django.test.client import Client
from django.urls import reverse


class TestHomeViews(TestCase):

    def setUp(self):
        self.client = Client()

    def test_home_view_GET(self):
        url = reverse('home')

        response = self.client.get(url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/home.html')
        