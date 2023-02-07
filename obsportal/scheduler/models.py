from django.db import models

class Event(models.Model):
    name = models.CharField('Event Name', max_length=120)
    event_date = models.DateTimeField()
    site = models.ForeignKey('devices.Site', on_delete=models.CASCADE)
    manager = models.CharField(max_length=120) 
    description = models.TextField(blank=True)
