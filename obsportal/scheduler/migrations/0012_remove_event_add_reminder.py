# Generated by Django 4.0.5 on 2023-03-30 21:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0011_event_add_reminder_reminder'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='add_reminder',
        ),
    ]
