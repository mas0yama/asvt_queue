import datetime

from django.db import models
from django.conf import settings


class Queue(models.Model):
    number = models.TextField(verbose_name='Номер', max_length=10)
    timestamp = models.DateTimeField(verbose_name='Время добавления', auto_now_add=True)
    person = models.ForeignKey(to='persons.Person', verbose_name='Человек',
                               related_name='queue_person_match', on_delete=models.CASCADE, unique=True)
    
    def __str__(self):
        return f'{self.number} {self.timestamp}'

    @property
    def left_time_secs(self):
        return (datetime.datetime.now - self.timestamp).total_seconds()
    
    @property
    def is_expired(self):
        return self.left_time_secs >= settings.WAIT_TIME_SECONDS
