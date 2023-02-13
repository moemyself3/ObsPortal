from django.db import models
from django.contrib import admin

class Event(models.Model):
    name = models.CharField('Event Name', max_length=120)
    event_start_datetime = models.DateTimeField('Start Time')
    event_end_datetime = models.DateTimeField('End Time')
    site = models.ForeignKey('devices.Site', on_delete=models.CASCADE, blank=True, null=True)
    routine = models.ForeignKey('routines.Routine', on_delete=models.CASCADE, blank=True, null=True)
    manager = models.CharField(max_length=120, blank=True) 
    description = models.TextField(blank=True)
