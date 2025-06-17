from django.urls import reverse
from django.http import HttpRequest
from django.test import TestCase, RequestFactory, LiveServerTestCase
from django.middleware.csrf import get_token

from Main.views import home, MainView

class HomePageTest(LiveServerTestCase):

    def test_home_page_return_correct_html(self):
        ''' Тест на правильно возвращаемый шаблон '''
        url = reverse('home')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'Main/home.html')

class ContactsPageTest(TestCase):
    ''' Тесты для страницы контактов '''
    def test_contacts_page_return_correct_html(self):
        ''' Тест на правильно возвращаемый шаблон '''
        url = reverse('contacts')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'Main/contacts.html')
    
    def test_contacts_feedback_form(self):
        ''' Тест на правильно отправляемую форму '''
        url = reverse('contacts')
        request = RequestFactory().get(url)
        # Симулируем отправку не правильной формы
        response = self.client.post(url, data={
            'username': 'testU',
            'email': 'some@gmail.com',     
            'message': 'MSG',
            'captcha_0': 'SOMEE',
            'csrfmiddlewaretoken': get_token(request)
        })
        self.assertEqual('✗ Возникла ошибка при отправке формы', response.context.get('feedback_message'))
        self.assertEqual(response.status_code, 200)