from django import forms
from django.contrib.admin import widgets
from .models import Event 

from datetime import datetime, timedelta

class AddEventForm(forms.ModelForm):
    event_start_datetime = forms.SplitDateTimeField(
            widget=forms.SplitDateTimeWidget(
                date_attrs={'type':'date'},
                time_attrs={'type':'time'}))

    event_end_datetime = forms.SplitDateTimeField(
            widget=forms.SplitDateTimeWidget(
                date_attrs={'type':'date'},
                time_attrs={'type':'time'}))
    
    def clean(self):
        super(AddEventForm, self).clean()

        start_datetime = self.cleaned_data.get('event_start_datetime')
        end_datetime = self.cleaned_data.get('event_end_datetime')

        if start_datetime >= end_datetime:
            self.errors['event_start_datetime'] = self.error_class([
                'Start time must be before the end time.'])

        if self.cleaned_data.get('repeat'):
            if not self.cleaned_data.get('interval'):
                self.errors['interval'] = self.error_class([
                    'An interval must be set.'])
            if not self.cleaned_data.get('frequency'):
                self.errors['frequency'] = self.error_class([
                    'A frequency must be set.'])
            if not self.cleaned_data.get('occurences'):
                self.errors['occurences'] = self.error_class([
                    'The number of occurences must be set.'])

    def recurring_event_handler(self):
        event_repeats = self.cleaned_data["repeat"]
        
        if event_repeats:
            event_start = self.cleaned_data["event_start_datetime"]
            event_end = self.cleaned_data["event_end_datetime"]
            event_duration = event_end - event_start
            occurences = self.cleaned_data["occurences"]

            kwargs = {str(self.cleaned_data["frequency"]) : self.cleaned_data["interval"]}
            
            next_event_timedelta = timedelta(**kwargs)

            new_start_datetime = event_start
            new_end_datetime = event_end

            event_data = dict(self.cleaned_data)
            recurring_event_list = [Event(**event_data), ]

            for occurence in range(occurences):
                event_data = dict(event_data)
                new_start_datetime = new_start_datetime + next_event_timedelta
                new_end_datetime = new_start_datetime + event_duration
                event_data["event_start_datetime"] = new_start_datetime
                event_data["event_end_datetime"] = new_end_datetime
                recurring_event_list.append(Event(**event_data))
            
            Event.objects.bulk_create(recurring_event_list)

    class Meta:
        model = Event
        fields = '__all__'
    
        widgets = { 
            'name': forms.CharField.widget(attrs={'class':'form-control'}),
            'site': forms.ChoiceField.widget(attrs={'class':'form-control'}),
            'manager': forms.ChoiceField.widget(attrs={'class':'form-control'}),
            'description': forms.CharField.widget(attrs={'class':'form-control'}),
            }


