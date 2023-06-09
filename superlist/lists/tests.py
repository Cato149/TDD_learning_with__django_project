from lists.models import Item, List
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


class ListAndItemModelTest(TestCase):
    '''тест модели элемента списка'''

    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()
        
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.list = list_
        second_item.save()
        
        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, 'Item the second')
        self.assertEqual(second_saved_item.list, list_)
        
        
class LisViewTest(TestCase):
    '''тест предсавления списка'''

    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertTemplateUsed(response, 'list.html')

    def test_display_all_list_items_for_that_list(self):
        '''тест отображает все элементы ТОЛЬКО ДЛЯ ЭТОГО списка'''
        correct_list = List.objects.create()
        Item.objects.create(text='itemey 1', list = correct_list)
        Item.objects.create(text='itemey 2', list = correct_list)
        other_list = List.objects.create()
        Item.objects.create(text='another itemey 1', list = other_list)
        Item.objects.create(text='another itemey 2', list = other_list)


        responce = self.client.get(f'/lists/{correct_list.id}/')

        self.assertContains(responce, 'itemey 1')
        self.assertContains(responce, 'itemey 2')
        self.assertNotContains(responce, 'another itemey 1')
        self.assertNotContains(responce, 'another itemey 2')
        
        
class NewListTest(TestCase):
    '''тест проверяет новые созданные списки'''

    def test_redirect_after_POST(self):
        '''тест перенаправляет после POST запроса'''
        responce = self.client.post('/lists/new', data={"item_text": "a new list item"})
        new_list = List.objects.first()

#       self.assertEqual(responce.status_code, 302)
#       self.assertRedirects(responce['location'], '/lists/the-only-one-list/')
        self.assertRedirects(responce, f'/lists/{new_list.id}/') #! <--- Заменяет две сткои выше

    def test_homepage_can_save_POST_request(self):
        '''тест может сохранять post-запрос'''
        self.client.post('/lists/new', data={"item_text": "a new list item"})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'a new list item')
        

class NewItemTest(TestCase):
    '''тест проверяет новой элемент списка'''
    
    def test_can_save_a_POST_request_to_an_a_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        
        self.client.post(
            f'/lists/{correct_list.id}/add_item',
            data={'item_text': 'A new item from an existing list'}
        )
        
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item from an existing list')
        self.assertEqual(new_item.list, correct_list)
    
    def test_can_redirect_to_list_view(self):
        '''тест проверяет перенаправление на представление листа'''
        other_list = List.objects.create()
        correct_list = List.objects.create()
        
        response = self.client.post(
            f'/lists/{correct_list.id}/add_item',
            data={'item_text': 'A new item from an existing list'}
        )
        self.assertRedirects(response, f'/lists/{correct_list.id}/', )
        
    def test_passes_correct_list_to_template(self):
        '''тест: представляется правильный шаблон списка'''
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get(f'/lists/{correct_list.id}/')
        
        self.assertEqual(response.context['list'], correct_list)
        