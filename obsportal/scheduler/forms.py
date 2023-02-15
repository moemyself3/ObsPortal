from django import forms
from django.contrib.admin import widgets

from .models import Event 

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
   
    class Meta:
        model = Event
        fields = '__all__'
    
        widgets = { 
            'name': forms.CharField.widget(attrs={'class':'form-control'}),
            'site': forms.ChoiceField.widget(attrs={'class':'form-control'}),
            'manager': forms.ChoiceField.widget(attrs={'class':'form-control'}),
            'description': forms.CharField.widget(attrs={'class':'form-control'}),
            }


