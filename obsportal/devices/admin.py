from django.contrib import admin

from .models import Device, Site

admin.site.register(Site)
admin.site.register(Device)
