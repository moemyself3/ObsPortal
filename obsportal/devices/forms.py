from django import forms
from django.http import HttpResponse
from django.forms.models import inlineformset_factory

from .models import Device, Site

from alpaca.management import configureddevices
from alpaca import discovery

class DiscoveryForm(forms.Form):
    discovery_port = forms.IntegerField(max_value=65535, min_value=1, required=False, widget=forms.IntegerField.widget(attrs={'class':'form-control'}))

    def alpaca_discovery(self):
        discovery_port = self.cleaned_data['discovery_port']
        default_discovery_port = discovery.port
        
        # Check for user defined discovery port
        if discovery_port is not None:
            discovery.port = discovery_port
        
        alpaca_device_servers = discovery.search_ipv4()
        
        devices = []
        if alpaca_device_servers:
            for server in alpaca_device_servers:
                alpacadevices = configureddevices(server)

                # Add server info to device information
                for device in alpacadevices:
                    device.update({"ServerAddress":server})
                
                devices.extend(alpacadevices)
                
        # Reset discovery port to default value
        discovery.port = default_discovery_port
        
        return devices

class RegisterDeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = '__all__'
    
        widgets = { 
            'site': forms.ChoiceField.widget(attrs={'class':'form-control'}),
            'ip_address': forms.GenericIPAddressField.widget(attrs={'class':'form-control'}),
            'devicetype': forms.ChoiceField.widget(attrs={'class':'form-control'}),
            'connected': forms.BooleanField.widget(attrs={'class':'form-check-input', 'disabled':'disabled'}),
            'description': forms.CharField.widget(attrs={'class':'form-control'}),
            'driverinfo': forms.CharField.widget(attrs={'class':'form-control'}),
            'driverversion': forms.IntegerField.widget(attrs={'class':'form-control'}),
            'interfaceversion': forms.IntegerField.widget(attrs={'class':'form-control'}),
            'devicename': forms.CharField.widget(attrs={'class':'form-control'}),
            'supportedactions': forms.JSONField.widget(attrs={'class':'form-control'}),
            }

class AddSiteForm(forms.ModelForm):
    class Meta:
        model = Site
        fields = '__all__'

        widgets = {
            'name': forms.CharField.widget(attrs={'class':'form-control'}),
            'geolat': forms.DecimalField.widget(attrs={'class':'form-control'}),
            'geolong': forms.DecimalField.widget(attrs={'class':'form-control'}),
            'elevation': forms.DecimalField.widget(attrs={'class':'form-control'}),
            }

# Formsets: Display multiple form inputs at once
SiteDeviceFormset = inlineformset_factory(Site, Device, exclude=('',))
