import os

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django_tables2 import SingleTableView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt

from . import models, tables
from utils import picture_scripts, string_scripts


@method_decorator(never_cache, name='dispatch')
class QueueListView(SingleTableView):
    model = models.Queue
    template_name = 'user_control/queue_list.html'
    table_class = tables.QueueTable

    def get_context_data(self, **kwargs):
        models.delete_old_records()
        return super().get_context_data(**kwargs)


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
    os.remove(person_to_call.person.path)
    person_to_call.person.delete()
    person_to_call.delete()
    return prepare_render(f'Вы вызвали человека с номером: {person_to_call.number}.')


@csrf_exempt
def upload_picture(request):
    if request.method == 'POST':
        picture = request.FILES['file']
        save_path = os.path.join(settings.PICTURES_STORE, string_scripts.cyrillic_to_latin(picture.name))
        with open(save_path, 'wb+') as destination:
            for chunk in picture.chunks():
                destination.write(chunk)

        if not picture_scripts.is_face_on_picture(save_path):
            os.remove(save_path)
            return JsonResponse({'answer': 'This is not a face'}, status=200)
        if picture_scripts.is_similar(models.Person.objects.values_list('path', flat=True), save_path):
            os.remove(save_path)
            return JsonResponse({'answer': 'Already in queue'}, status=200)
        person = models.Person(path=save_path)
        person.save()
        number = models.add_to_queue(models.get_last_number() + 1, person)

        return JsonResponse({'answer': number}, status=200)
    return JsonResponse({'answer': 'This HTTP method is prohibited'}, status=405)
