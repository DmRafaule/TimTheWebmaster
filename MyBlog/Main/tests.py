from django.urls import reverse
from django.http import HttpRequest
from django.test import TestCase
from .views import home

class HomePageTest(TestCase):

    def test_home_page_return_correct_html(self):
        # Тест на правильно возвращаемый контент
        url = reverse('home')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'Main/home.html')