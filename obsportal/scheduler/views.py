from django.shortcuts import render
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils import timezone

from .forms import AddEventForm, EventReminderFormset
from .models import Event, Category
from .tasks import send_admin_notification_mail

import calendar

from datetime import datetime
from datetime import date

# Schedule views
class EventListView(ListView):
    model = Event
    template_name = 'scheduler/schedule.html'
    queryset = Event.objects.order_by('event_start_datetime').filter(event_start_datetime__gt=timezone.now())
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
                '<table ', '<table class="table table-striped table-hover table-sm" '
                )

        current_calendar = current_calendar.replace(
                '<td ', '<td width="50" height="50"'
                )
        current_calendar = current_calendar.replace(
                '>'+str(current_day)+'<',
                'style="background-color:#FFDD33;">'+str(current_day)+'<')

        for day in calendar.Calendar().itermonthdays(year=current_year, month=current_month):
            if day != 0:
                event_count = self.model.objects.filter(
                        event_start_datetime__day=day,
                        event_start_datetime__month=current_month).count()
                
                if event_count == 0:
                    event_count = ''
                    event_pill_tag = {
                        'open':'',
                        'close':''
                        }
                else:
                    event_pill_tag = {
                        'open': '<span class="position-absolute top-0 start-100'
                                ' translate-middle badge rounded-pill bg-danger"> ',
                        'close':'</span>'
                        }
                calendar_date = date(year=current_year, month=current_month, day=day)
                current_calendar = current_calendar.replace(
                        '>' + str(day) + '<',
                        '><a href=' + reverse_lazy('scheduler:event-lookup') +
                        '?date='+ str(calendar_date) +
                        ' class="btn btn-light w-100 position-relative"'
                        ' role="button" '
                        ' data-bs-toggle="tooltip" data-bs-title='
                        ' "click to see events"'
                        ' >'+ str(day) + event_pill_tag['open'] +
                        str(event_count) + event_pill_tag['close'] + ' </a><'
                        )
        context['calendar'] = current_calendar
        return context


class EventCreateView(SuccessMessageMixin, CreateView):
    template_name= 'scheduler/addevent.html'
    form_class = AddEventForm
    success_url = reverse_lazy('scheduler:index')
    success_message = "%(name)s was created successfully"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data["reminders"] = EventReminderFormset(self.request.POST)
        else:
            data["reminders"] = EventReminderFormset()
        return data

    def form_valid(self, form):
        form.recurring_event_handler()
        context = self.get_context_data()
        reminders = context["reminders"]
        self.object = form.save()

        if reminders.is_valid():
            reminders.instance = self.object
            reminders.save()
            # Returns the queryset of all Reminder objects related to the Event
            reminder_set = reminders.instance.reminder_set.all()
            
            # set Celery task
            for reminder in reminder_set:
                message = f"""
                    Event Reminder for {reminder.event}! 
                    The event is set to start in {reminder.interval} {reminder.timeunit}
                    """
                
                send_admin_notification_mail.apply_async(eta=reminder.ETA, kwargs={'message' : message })

        return super().form_valid(form)

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
                    ).order_by('event_start_datetime')
    
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

