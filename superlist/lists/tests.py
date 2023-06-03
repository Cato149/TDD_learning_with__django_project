from django.http import HttpRequest
from django.test import TestCase
from django.urls import resolve

from lists.views import home_page


class HomePageTest(TestCase):    
        
    def test_uses_home_template(self):
        '''Тест: Домашнаяя страница возвращает html'''
        response = self.client.get('/')
        
        html = response.content.decode('utf8')
        self.assertTrue(html.startswith('<html>'))
        self.assertIn('<title>To-Do list</title>', html)
        self.assertTrue(html.endswith('</html>'))
        
        self.assertTemplateUsed(response, 'home.html')