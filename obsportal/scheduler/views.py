from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy

from .forms import AddEventForm
from .models import Event

import calendar

from calendar import HTMLCalendar
from datetime import datetime

# Schedule views
class EventListView(ListView):
    model = Event
    template_name = 'scheduler/schedule.html'
    context_object_name = 'event_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #get current datetime
        now = datetime.now()
        year = now.year
        month = now.month
        day = now.day
    
        calendar = HTMLCalendar().formatmonth(year, month)
        calendar = calendar.replace(
                '<table ', '<table class="table table-striped table-hover" '
                )

        calendar = calendar.replace(
                '<td ', '<td  width="50" height="50"'
                )

        calendar = calendar.replace(
                '>'+str(day)+'<',
                'style="background-color:#FFDD33; border:1px solid black; border-radius: 100px;">'+str(day)+'<')
        context['calendar'] = calendar
        return context


class EventCreateView(SuccessMessageMixin, CreateView):
    template_name= 'scheduler/addevent.html'
    form_class = AddEventForm
    success_url = reverse_lazy('scheduler:index')
    success_message = "%(name)s was created successfully"
