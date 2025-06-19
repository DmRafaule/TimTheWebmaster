from django.urls import reverse
from django.test import RequestFactory, LiveServerTestCase
from django.middleware.csrf import get_token

class HomePageTest(LiveServerTestCase):
    ''' Тесты для домашней страницы '''

    def test_home_page_return_correct_html(self):
        ''' Тест на правильно возвращаемый шаблон '''
        url = reverse('home')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'Main/home.html')

class ContactsPageTest(LiveServerTestCase):
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

class AboutPageTest(LiveServerTestCase):
    ''' Тесты для страницы ОБ '''

    def test_about_page_return_correct_html(self):
        ''' Тест на правильно возвращаемый шаблон для страницы about'''
        url = reverse('about')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'Main/about.html')

class Page404Test(LiveServerTestCase):
    ''' Тесты для страницы 404 '''

    def test_404_page_return_correct_html(self):
        ''' Тест на правильно возвращаемый шаблон '''
        response = self.client.get('sdkfjsdfsdfoijoew')
        self.assertTemplateUsed(response, 'Main/404.html')
