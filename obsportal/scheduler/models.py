from django.db import models
from django.contrib import admin

class Category(models.Model):
    name = models.CharField('Category', max_length=50, unique=True)
   
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

def defaultCategoryId():
    category_id = Category.objects.get_or_create(name='Uncategorized')[0].pk
    return category_id


class Event(models.Model):
    FREQUENCY_CHOICES = [
            ('second', 'second'),
            ('minute', 'minute'),
            ('hour', 'hour'),
            ('day', 'day'),
            ('week', 'week'),
            ('month', 'month'),
            ('year', 'year'),
            ]

    name = models.CharField('Event Name', max_length=120)
    event_start_datetime = models.DateTimeField('Start Time')
    event_end_datetime = models.DateTimeField('End Time')
    repeat = models.BooleanField(default=False)
    interval = models.PositiveSmallIntegerField('Interval', blank=True, null=True)
    frequency = models.CharField('Frequency', choices=FREQUENCY_CHOICES, max_length=10, blank=True, null=True)
    site = models.ForeignKey('devices.Site', on_delete=models.CASCADE, blank=True, null=True)
    routine = models.ForeignKey('routines.Routine', on_delete=models.CASCADE, blank=True, null=True)
    manager = models.CharField(max_length=120, blank=True) 
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_DEFAULT, default=defaultCategoryId)

    def __str__(self):
        return self.name + ' | ' + str(self.event_start_datetime)
