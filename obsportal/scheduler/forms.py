from django import forms

from .models import Event 

class AddEventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'
    
        widgets = { 
            'name': forms.CharField.widget(attrs={'class':'form-control'}),
            'event_start_datetime': forms.SplitDateTimeField.widget(
                date_attrs={'type':'date'}, 
                time_attrs={'type':'time'}
                ),
            'event_end_datetime': forms.SplitDateTimeField.widget(
                date_attrs={'type':'date'},
                time_attrs={'type':'time'}
                ),
            'site': forms.ChoiceField.widget(attrs={'class':'form-control'}),
            'manager': forms.ChoiceField.widget(attrs={'class':'form-control'}),
            'description': forms.CharField.widget(attrs={'class':'form-control'}),
            }


