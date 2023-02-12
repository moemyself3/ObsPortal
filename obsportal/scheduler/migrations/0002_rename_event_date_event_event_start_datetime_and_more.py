# Generated by Django 4.0.5 on 2023-02-11 23:00

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0006_device_port'),
        ('scheduler', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='event_date',
            new_name='event_start_datetime',
        ),
        migrations.AddField(
            model_name='event',
            name='event_end_datetime',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='event',
            name='site',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='devices.site'),
        ),
    ]
