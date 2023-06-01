from django.test import TestCase

class SomkeTest(TestCase):
    '''тест на токсичность'''
    
    def test_bad_maths(self):
        '''Тест  на нерпавильные рассчеты'''
        self.assertEqual(1 + 1, 3)