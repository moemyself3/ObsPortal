from django.contrib import admin

from .models import Event, Category, Reminder

admin.site.register(Event)
admin.site.register(Category)
admin.site.register(Reminder)
