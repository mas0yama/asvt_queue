# Generated by Django 4.1.9 on 2025-01-12 16:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_control', '0002_alter_queue_person'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='queue',
            options={'ordering': ('timestamp',)},
        ),
    ]
