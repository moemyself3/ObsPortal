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
        now = timezone.make_aware(datetime.now())
        year = now.year
        month = now.month
        day = now.day
        
        # Calendar and formatting
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

class CategoryCreateView(SuccessMessageMixin, CreateView):
    model = Category
    fields = ['name']
    template_name = 'scheduler/addcategory.html'
    success_url = reverse_lazy('scheduler:index')
    success_message = "%(name)s was created successfully"

