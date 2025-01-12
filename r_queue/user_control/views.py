from django.shortcuts import render
from django_tables2 import SingleTableView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator

from . import models, tables
from persons.models import Person
from utils import camera_scripts, picture_scripts

@method_decorator(never_cache, name='dispatch')
class QueueListView(SingleTableView):
    model = models.Queue
    template_name = 'user_control/queue_list.html'
    table_class = tables.QueueTable

    def get_context_data(self, **kwargs):
        models.delete_old_records()
        return super().get_context_data(**kwargs)


def add_to_queue(request):
    def prepare_render(answer_text):
        return render(request, 'user_control/queue_answer.html', {'answer_text': answer_text})
    picture = camera_scripts.take_picture()
    if not picture_scripts.is_face_on_picture(picture):
        return prepare_render('На фото не удалось распознать лицо, попробуйте еще раз.')
    similar_person = picture_scripts.get_similar(
        Person.objects.values('id', 'picture'), picture)
    if len(similar_person) > 1:
        return prepare_render('На фото не удалось распознать лицо, попробуйте еще раз.')
    if len(similar_person) == 1:
        try:
            person = models.Queue.objects.get(person=similar_person[0])
            if person.is_expired:
                # удалить
                # добавить
                number = '12345'
                return prepare_render(f'Вы успешно встали в очередь. Ваш номер: {number}.')
            return prepare_render(f'Вы уже встали в очередь и сможете сделать это повторно через {person.left_time_secs}')
        except models.Queue.DoesNotExist:
            pass
    number = models.add_to_queue(models.get_last_number() + 1, picture, create_person=True)
    return prepare_render(f'Вы успешно встали в очередь. Ваш номер: {number}.')


@method_decorator(never_cache, name='dispatch')
class QueueListProtectedView(LoginRequiredMixin, SingleTableView):
    model = models.Queue
    template_name = 'user_control/queue_list.html'
    table_class = tables.QueueTable

    def get_context_data(self, **kwargs):
        models.delete_old_records()
        context = super().get_context_data(**kwargs)
        context.update({'is_manager': True})
        return context


@login_required
def call_next_person(request):
    def prepare_render(answer_text):
        return render(request, 'user_control/queue_answer.html', {'answer_text': answer_text})
    queue = models.Queue.objects.all()
    if not queue:
        return prepare_render('Очередь пустая, нельзя вызвать человека.')
    person_to_call = queue.first()
    person_to_call.person.delete()
    person_to_call.delete()
    return prepare_render(f'Вы вызвали человека с номером: {person_to_call.number}.')
