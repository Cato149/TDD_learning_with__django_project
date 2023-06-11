from django.db import models

# Create your models here.

class List(models.Model):
    '''Это список'''
    pass

class Item(models.Model):
    '''Эллемент списка'''
    text = models.TextField(default="")
    list = models.ForeignKey(List, on_delete=models.CASCADE, default=None)
