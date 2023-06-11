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

    def test_homepage_can_save_POST_request(self):
        '''тест может сохранять post-запрос'''
        self.client.post('/', data={"item_text": "a new list item"})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'a new list item')

    def test_redirect_after_POST(self):
        '''тест перенаправляет после POST запроса'''
        responce = self.client.post('/', data={"item_text": "a new list item"})

        self.assertEqual(responce.status_code, 302)
        self.assertEqual(responce['location'], '/lists/the-only-one-list/')

    def test_only_saves_item_when_necessary(self):
        '''тест сохранает элементы только тогда, когда нужно'''
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)


class LisViewTest(TestCase):
    '''тест предсавления списка'''
    
    def test_uses_list_tmplates(self):
        responce = self.client.get('/lists/the-only-one-list/')
        self.assertTemplateUsed(responce, 'list.html')

    def test_display_all_list_items(self):
        '''тест отображает все элементы списка'''
        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')

        responce = self.client.get('/lists/the-only-one-list/')

        self.assertContains(responce, 'itemey 1')
        self.assertContains(responce, 'itemey 2')
