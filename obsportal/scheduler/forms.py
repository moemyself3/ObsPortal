from django import forms

from .models import Event 

class AddEventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'
    
        widgets = { 
            'name': forms.CharField.widget(attrs={'class':'form-control'}),
            'event_date': forms.DateTimeField.widget(attrs={'id':'datetimepicker'}),
            'site': forms.ChoiceField.widget(attrs={'class':'form-control'}),
            'manager': forms.ChoiceField.widget(attrs={'class':'form-control'}),
            'description': forms.CharField.widget(attrs={'class':'form-control'}),
            }


