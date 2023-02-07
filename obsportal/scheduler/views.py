from django.shortcuts import render
from django.views.generic import ListView

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
    calendar = calendar.replace('<td ', '<td  width="150" height="150"')
    return render(request, 'scheduler/schedule.html', {'calendar': calendar})
