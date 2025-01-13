from django.db import models

class Person(models.Model):
    path = models.TextField(verbose_name='Путь к фото', unique=True)

    def __str__(self):
        return self.path
