from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

from .forms import AddEventForm

import calendar

from calendar import HTMLCalendar
from datetime import datetime

# Schedule views
#class ScheduleListView(ListView):
#    model = Schedule
#    template_name = 'scheduler/schedule.html'
#    context_object_name = 'schedule_list'

def CalendarView(request):
    #get current datetime
    now = datetime.now()
    year = now.year
    month = now.month

    calendar = HTMLCalendar().formatmonth(year, month)
    calendar = calendar.replace('<td ', '<td  width="50" height="50"')
    return render(request, 'scheduler/schedule.html', {'calendar': calendar})

class EventCreateView(SuccessMessageMixin, CreateView):
    template_name= 'scheduler/addevent.html'
    form_class = AddEventForm
    success_message = "%(name)s was created successfully"
