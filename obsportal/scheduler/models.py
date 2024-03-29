from django.db import models
from django.contrib import admin
from django.core.validators import MaxValueValidator, MinValueValidator

from datetime import datetime, timedelta

TIME_UNIT_CHOICES = [
                        ('seconds', 'seconds'),
                        ('minutes', 'minutes'),
                        ('hours', 'hours'),
                        ('days', 'days'),
                        ('weeks', 'weeks'),
                        ('months', 'months'),
                        ('years', 'years'),
                     ]


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
    name = models.CharField('Event Name', max_length=120)
    event_start_datetime = models.DateTimeField('Start Time')
    event_end_datetime = models.DateTimeField('End Time')
    repeat = models.BooleanField(default=False)
    interval = models.PositiveSmallIntegerField(
            'Interval (1-100)',
            blank=True,
            null=True,
            validators=[MinValueValidator(1),
                        MaxValueValidator(100)]
            )
    frequency = models.CharField('Frequency', choices=TIME_UNIT_CHOICES, max_length=10, blank=True, null=True)
    occurences = models.PositiveSmallIntegerField(
            'Occurences (1-100)', 
            blank=True, 
            null=True, 
            validators=[MinValueValidator(1),
                        MaxValueValidator(100)]
            )

    site = models.ForeignKey('devices.Site', on_delete=models.CASCADE, blank=True, null=True)
    routine = models.ForeignKey('routines.Routine', on_delete=models.CASCADE, blank=True, null=True)
    manager = models.CharField(max_length=120, blank=True) 
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_DEFAULT, default=defaultCategoryId)

    def __str__(self):
        return self.name + ' at ' + str(self.event_start_datetime)


class Reminder(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    interval = models.PositiveSmallIntegerField(
            'Interval (1-100)',
            blank=True,
            null=True,
            validators=[MinValueValidator(1),
                        MaxValueValidator(100)]
            )
    timeunit = models.CharField('Unit of Time', choices=TIME_UNIT_CHOICES, max_length=10, blank=True, null=True)

    def __str__(self):
        return self.event.name + ' | ETA ' + str(self.ETA)

    @property
    def ETA(self):
        kwargs = {str(self.timeunit) : self.interval}    
        reminder_timedelta = timedelta(**kwargs)
        eta = self.event.event_start_datetime - reminder_timedelta
        return eta

