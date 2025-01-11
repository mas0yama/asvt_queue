from django.urls import path

from . import views

urlpatterns = [
    path('', views.QueueListView.as_view(), name='queue_list'),
    path('add/', views.add_to_queue, name='queue_add'),
    path('call_next/', views.call_next_person, name='queue_call_next'),
]
