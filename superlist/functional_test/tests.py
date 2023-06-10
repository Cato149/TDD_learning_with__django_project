from django.test import LiveServerTestCase
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import unittest
from selenium.common.exceptions import WebDriverException 

MAX_WAIT = 10

class NewVisorTest(LiveServerTestCase):
    '''тест нового посетителя'''
    
    def setUp(self):
        '''утсановка'''
        self.browser = webdriver.Firefox()
        
    def tearDown(self):
        '''Демонотаж'''
        self.browser.quit()
        
    def wait_for_row_in_list(self, row_text):
        '''Ожидает строку в таблице списка дел'''
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element(By.ID, 'id_list_table')
                rows = table.find_elements(By.TAG_NAME, 'tr')
                self.assertIn('1: Купить молоко', [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)
    
    def test_can_start_a_list_for_one_user(self):
        '''тест: тможно начать список и получить его позже'''
        #Мэту посоветоали новое крутое приложение для ведни списка дел
        self.browser.get(self.live_server_url)
        
        #Он видит, что заголовок и шапка говорят о списке дел (to-do)
        self.assertIn('To-Do list', self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME, 'h1').text
        self.assertIn('To-Do', header_text)
        
        #Он видит поле ввода новой задачи
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )
        
        #Решает попробовать созать тебе дело на завтра. вводит: "Купить по пути домой молоко"
        inputbox.send_keys('Купить молоко')

        # Нажав сохранить страница перезагружается и теперь Мэт видит поле ввода и задачу, которую только что добавил
        inputbox.send_keys(Keys.ENTER)
        
#        self.assertTrue(
#            any(row.text == '1: Купить молоко' for row in rows), 
#            "Новый элемент не появился в таблице. Содержимым было: " 
#            f"{table.text}"
#        )
        self.wait_for_row_in_list('1: Купить молоко')
        # Он добавляет еще пару задач
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('Купить мясо')
        inputbox.send_keys(Keys.ENTER)
        # Страница обновившись показыват каждый новый элемент
        self.wait_for_row_in_list('1: Купить молоко')
        self.wait_for_row_in_list('2: Купить мясо')
        # Мэт решает сохранить свой список. Он нажимает на кнопку и страница генерирует для него 
        # URL по которому он может получить доступ к своему списку откуда удобно
        self.fail('Закончить тест!')
        # Он переходит по ссылке и видит свой список 

        # Наконец сайт выдыхает, ведь этот душнила ушел
        
    def test_multiple_users_can_start_lists_at_differtnt_users(self):
        '''тест: многочисленные пользователи могут начать список по разным URL'''
            
        #Мэт решает начать новый список
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        inputbox.send_keys('Купить молоко')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list('1: Купить молоко')
        
        # Мэт решает сохранить свой список. Он нажимает на кнопку и страница генерирует для него 
        # URL по которому он может получить доступ к своему списку откуда удобно
        mat_list_url = self.browser.current_url
        self.assertRegex(mat_list_url, '/lists/.+')
        
        # на сайт пришел новый пользоватлеь Боб
        #№ мы использует новый сеант браузера чтобы не пришла информация от Эдит
        self.browser.quit()
        self.browser = webdriver.Firefox()
        
        # Боб посещает страницу. Тут нет ничего, чтобы наопминало о пристутвии Мэта
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertNotIn('Купить молоко', page_text)
        self.assertNotIn('Купить ммясо', page_text) 

        # боб начинает новый список
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('Забрать Молли из садика')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list('1: Забрать Молли из садика')

        # Боб получает уникальный URL
        bob_list_url = self.browser.current_url
        self.assertRegex(bob_list_url, '/lists/.+')
        self.assertNotEqual(bob_list_url, mat_list_url)
        
        # ничего не говорит о присутвии Мэта ранее
        page_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertNotIn('Купить молоко', page_text)
        self.assertIn('Забрать Молли из садика', page_text)
        
        
if __name__ == '__main__':
    unittest.main()
    