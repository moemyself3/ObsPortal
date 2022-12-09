from django.db import models
from django.urls import reverse

from .site import Site


class Device(models.Model):
    site = models.ForeignKey(
           'Site',
            on_delete=models.CASCADE,
            related_name='device_site',
            )
    devicename = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField('IP Address', null=True)
    port = models.IntegerField(null=True)
    devicetype = models.CharField(max_length=100, null=True)
    connected = models.BooleanField(default=False)
    description = models.CharField(max_length=255)
    driverinfo = models.CharField(max_length=255)
    driverversion = models.CharField(max_length=255)
    interfaceversion = models.IntegerField()
    supportedactions = models.JSONField()

    def get_absolute_url(self):
        return reverse('devices:device-detail', kwargs={'pk':self.pk})
