from django.shortcuts import render
from django_tables2 import SingleTableView

from . import models, tables
from persons.models import Person
from utils import camera_scripts, picture_scripts


class QueueListView(SingleTableView):
    model = models.Queue
    template_name = 'user_control/queue_list.html'
    table_class = tables.QueueTable


def call_next_person(request):
    pass


def add_to_queue(request):
    def prepare_render(context):
        return render(request, 'user_control/add_to_queue_answer.html', context)
    picture = camera_scripts.take_picture()
    if not picture_scripts.is_face_on_picture(picture):
        return prepare_render({'answer_text': 'На фото не удалось распознать лицо, попробуйте еще раз.'})
    similar_person = picture_scripts.get_similar(
        Person.objects.values('id', 'picture'), picture)
    if len(similar_person) > 1:
        return prepare_render({'answer_text': 'На фото не удалось распознать лицо, попробуйте еще раз.'})
    if len(similar_person) == 1:
        try:
            person = models.Queue.objects.get(person=similar_person[0])
            if person.is_expired:
                # удалить
                # добавить
                number = '12345'
                return prepare_render({'answer_text': f'Вы успешно встали в очередь. Ваш номер: {number}.'})
            return prepare_render({'answer_text': f'Вы уже встали в очередь и сможете сделать это повторно через',
                                   'left_time': person.left_time_secs})
        except models.Queue.DoesNotExist:
            pass
    # добавить
    number = '12345'
    return prepare_render({'answer_text': f'Вы успешно встали в очередь. Ваш номер: {number}.'})
