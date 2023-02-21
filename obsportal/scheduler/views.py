from django.shortcuts import render
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils import timezone

from .forms import AddEventForm
from .models import Event, Category

import calendar

from datetime import datetime
from datetime import date

# Schedule views
class EventListView(ListView):
    model = Event
    template_name = 'scheduler/schedule.html'
    context_object_name = 'event_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        #get current datetime
        now = timezone.make_aware(datetime.now())
        current_year = now.year
        current_month = now.month
        current_day = now.day
        
        # Calendar and formatting
        current_calendar = calendar.HTMLCalendar().formatmonth(current_year, current_month)
        current_calendar = current_calendar.replace(
                '<table ', '<table class="table table-striped table-hover" '
                )

        current_calendar = current_calendar.replace(
                '<td ', '<td  width="50" height="50"'
                )

        current_calendar = current_calendar.replace(
                '>'+str(current_day)+'<',
                'style="background-color:#FFDD33;">'+str(current_day)+'<')

        for day in calendar.Calendar().itermonthdays(year=current_year, month=current_month):
            if day != 0:
                calendar_date = date(year=current_year, month=current_month, day=day)
                current_calendar = current_calendar.replace(
                        '>' + str(day) + '<',
                        '><a href=' + reverse_lazy('scheduler:event-lookup') +
                        '?date='+ str(calendar_date) +
                        ' class="btn btn-light w-100" role="button" '
                        'data-bs-toggle="tooltip" data-bs-title="Default tooltip"'
                        ' >'+ str(day) + '</a><'
                        )
        context['calendar'] = current_calendar
        return context


class EventCreateView(SuccessMessageMixin, CreateView):
    template_name= 'scheduler/addevent.html'
    form_class = AddEventForm
    success_url = reverse_lazy('scheduler:index')
    success_message = "%(name)s was created successfully"

class EventDetailView(DetailView):
    model = Event
    template_name = 'scheduler/detailevent.html'

class EventUpdateView(SuccessMessageMixin, UpdateView):
    model = Event
    form_class = AddEventForm
    template_name = 'scheduler/updateevent.html'
    success_url = reverse_lazy('scheduler:index')
    success_message = "Event was updated successfully"

class EventDeleteView(SuccessMessageMixin, DeleteView):
    model = Event
    template_name= 'scheduler/deleteevent.html'
    success_url = reverse_lazy('scheduler:index')
    success_message = "Event was deleted successfully"

class EventLookupView(ListView):
    model = Event
    template_name = 'scheduler/eventlookup.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET.get('date') is not None:
            context['search_date'] = self.request.GET.get('date')
        else:
            #get current datetime
            now = timezone.make_aware(datetime.now())
            year = now.year
            month = now.month
            day = now.day
    
            event_list = Event.objects.filter(
                    event_start_datetime__year = year,
                    event_start_datetime__month = month
                    )
    
            context['event_list'] = event_list
            context['search_date'] = now.strftime('%B %Y')
        return context

    def get_queryset(self):
        query = self.request.GET.get('date')
        event_list = Event.objects.filter(
                event_start_datetime__date = query
                )
        return event_list


class CategoryCreateView(SuccessMessageMixin, CreateView):
    model = Category
    fields = ['name']
    template_name = 'scheduler/addcategory.html'
    success_url = reverse_lazy('scheduler:index')
    success_message = "%(name)s was created successfully"

