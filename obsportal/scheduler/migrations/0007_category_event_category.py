# Generated by Django 4.0.5 on 2023-02-15 22:00

from django.db import migrations, models
import django.db.models.deletion
import scheduler.models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0006_alter_event_routine_alter_event_site'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Category')),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='category',
            field=models.ForeignKey(default=scheduler.models.defaultCategoryId, on_delete=django.db.models.deletion.SET_DEFAULT, to='scheduler.category'),
        ),
    ]
