# Generated by Django 4.0.5 on 2023-02-13 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0004_event_routine'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='manager',
            field=models.CharField(blank=True, max_length=120),
        ),
    ]
