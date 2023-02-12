from django.db import models

class Event(models.Model):
    name = models.CharField('Event Name', max_length=120)
    event_start_datetime = models.DateTimeField('Start Time')
    event_end_datetime = models.DateTimeField('End Time')
    site = models.ForeignKey('devices.Site', on_delete=models.CASCADE, blank=True)
    routine = models.ForeignKey('routines.Routine', on_delete=models.CASCADE, blank=True)
    manager = models.CharField(max_length=120) 
    description = models.TextField(blank=True)
