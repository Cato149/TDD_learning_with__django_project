from lists.models import Item
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
        
    def test_can_save_a_POST_request(self):
        '''Тест может сохранить POST запрос'''
        responce = self.client.post('/', data={'item_text': 'A new list item'})
        self.assertIn('A new list item', responce.content.decode())
        self.assertTemplateUsed(responce, 'home.html')
        
        
class ItemModelTest(TestCase):
    '''тест модели элемента списка'''
    
    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.save()
        
        second_item = Item()
        second_item.text = 'Item the second'
        second_item.save()
        
        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)
        
        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(second_saved_item.text, 'Item the second')
        