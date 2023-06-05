from django.db import models

# Create your models here.

class Item(models.Model):
    '''Эллемент списка'''
    text = models.TextField(default="")
