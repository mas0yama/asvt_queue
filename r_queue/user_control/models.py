import datetime

from django.db import models
from django.conf import settings
from django.utils import timezone

from persons.models import Person


class Queue(models.Model):
    number = models.TextField(verbose_name='Номер', max_length=10, unique=True)
    timestamp = models.DateTimeField(verbose_name='Время добавления', auto_now_add=True)
    person = models.ForeignKey(to='persons.Person', verbose_name='Человек',
                               related_name='queue_person_match', on_delete=models.CASCADE, unique=True)

    def __str__(self):
        return f'{self.number} {self.timestamp}'

    @property
    def left_time_secs(self):
        return (timezone.now() - self.timestamp).total_seconds()

    @property
    def is_expired(self):
        return self.left_time_secs >= settings.WAIT_TIME_SECONDS


def delete_old_records():
    records_to_delete = tuple(q for q in Queue.objects.all() if q.is_expired)
    for record in records_to_delete:
        record.person.delete()
        record.delete()


def get_last_number():
    prefix = datetime.datetime.now().strftime("%d%m")
    last_number = 0
    for number in Queue.objects.values_list('number', flat=True):
        if not number.startswith(prefix):
            continue
        last_number = int(number[5:]) if int(number[5:]) > last_number else last_number

    return last_number


def add_to_queue(number, person, create_person=False):
    if create_person:
        person = Person(picture=person)
        person.save()
    else:
        person = Person.objects.get(pk=person)
    number = f'{datetime.datetime.now().strftime("%d%m")}#{number}'
    q_obj = Queue(number=number, person=person)
    q_obj.save()
    return number
