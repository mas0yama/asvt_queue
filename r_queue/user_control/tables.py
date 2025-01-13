import django_tables2 as tables

from . import models
from design.tables import TableStyleMeta


class QueueTable(tables.Table):
    number = tables.Column(verbose_name='Номер', orderable=False)
    timestamp = tables.DateTimeColumn(verbose_name='В очереди с', orderable=False, format='d M, H:i:s')
    cabinet = tables.Column(verbose_name='Кабинет', orderable=False)

    class Meta(TableStyleMeta):
        model = models.Queue
        fields = 'number', 'timestamp', 'cabinet',
