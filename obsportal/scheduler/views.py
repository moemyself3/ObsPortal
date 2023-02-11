from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

from .forms import AddEventForm
from .models import Event

import calendar

from calendar import HTMLCalendar
from datetime import datetime

# Schedule views
class EventListView(ListView):
    model = Event
    template_name = 'scheduler/schedule.html'
    context_object_name = 'schedule_list'

    def get(self, request, *args, **kwargs):
        #get current datetime
        now = datetime.now()
        year = now.year
        month = now.month
        day = now.day
    
        calendar = HTMLCalendar().formatmonth(year, month)
        calendar = calendar.replace('<td ', '<td  width="50" height="50"')
        calendar = calendar.replace(
                '>'+str(day)+'<',
                'style="background-color:#FFDD33; border:1px solid black; border-radius: 100px;">'+str(day)+'<')
        return render(request, 'scheduler/schedule.html', {'calendar': calendar})

class EventCreateView(SuccessMessageMixin, CreateView):
    template_name= 'scheduler/addevent.html'
    form_class = AddEventForm
    success_message = "%(name)s was created successfully"
