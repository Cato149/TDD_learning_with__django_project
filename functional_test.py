import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import unittest


class NewVisorTest(unittest.TestCase):
    '''тест нового посетителя'''
    
    def setUp(self):
        '''утсановка'''
        self.browser = webdriver.Firefox()
        
    def tearDown(self):
        '''Демонотаж'''
        self.browser.quit()
    
    def test_can_start_a_list_and_retrever_it_later(self):
        '''тест: тможно начать список и получить его позже'''
        #Мэту посоветоали новое крутое приложение для ведни списка дел
        self.browser.get('http://localhost:8000')
        
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
        time.sleep(1)
        
        table = self.browser.find_element(By.ID, 'id_list_table')
        rows = table.find_elements(By.TAG_NAME, 'tr')
#        self.assertTrue(
#            any(row.text == '1: Купить молоко' for row in rows), 
#            "Новый элемент не появился в таблице. Содержимым было: " 
#            f"{table.text}"
#        )
        self.assertIn('1: Купить молоко', [row.text for row in rows])
        # Он добавляет еще пару задач
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('Купить мясо')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        # Страница обновившись показыват каждый новый элемент
        table = self.browser.find_element(By.ID, 'id_list_table')
        rows = table.find_elements(By.TAG_NAME, 'tr')
        self.assertIn('1: Купить молоко', [row.text for row in rows])
        self.assertIn('2: Купить мясо', [row.text for row in rows])

        # Мэт решает сохранить свой список. Он нажимает на кнопку и страница генерирует для него 
        # URL по которому он может получить доступ к своему списку откуда удобно
        self.fail('Закончить тест!')
        # Он переходит по ссылке и видит свой список 

        # Наконец сайт выдыхает, ведь этот душнила ушел

        
if __name__ == '__main__':
    unittest.main()
    