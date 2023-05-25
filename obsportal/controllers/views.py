from django.shortcuts import render
from django.views.generic import DetailView, ListView
from django.http import HttpResponse

from devices.models import Site, Device
from devices.models import Telescope as modelT

from alpaca.telescope import Telescope
from alpaca.camera import Camera
from alpaca.device import Device as Devicebase
from alpaca.exceptions import AlpacaRequestException
from requests.exceptions import ConnectTimeout
from datetime import timedelta, datetime

from .tasks import telescope_demo

from enum import Enum

# Main control window
class IndexView(ListView):
    model = Site
    template_name = 'controllers/index.html'
    context_object_name = 'sites'

class SiteDetailView(DetailView):
    model = Site
    template_name = 'controllers/site.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sites'] = Site.objects.all()
        return context

def TelescopeDemoView(request):
    model = Site
    context = {"sites":Site.objects.all(), }
    telescope_demo.apply_async()
    return render(request, "controllers/index.html", context)

## htmx views
def DeviceView(request, device_id):
    if device_id:
        device = Device.objects.get(pk=device_id)
        context = {
                    "device_id": device_id,
                    "device_type": device.devicetype,
                }
        context["device"] = {}
        alpaca_device, context = device_properties(device, context)
        
        if alpaca_device.device_type == "telescope":
            if request.method == "PUT":
                if alpaca_device.Tracking:
                    alpaca_device.Tracking = False
                else:
                    alpaca_device.Tracking = True

            telescope = alpaca_device
            context["telescope"] = {
                    "tracking": telescope.Tracking,
                    "slewing": telescope.Slewing,
                    "parking": telescope.AtPark,
                    "telescope_utcdate": telescope.UTCDate,
                    "ra": telescope.RightAscension,
                    "dec": telescope.Declination,
                    "alt": telescope.Altitude,
                    "az": telescope.Azimuth,
                    }
            return render(request, "controllers/fragments/telescope.html", context)

    return render(request, "controllers/fragments/device.html", context)

def device_properties(device, context):
    device_fields = Device._meta.get_fields()
    device_fieldname = [device_field.name for device_field in device_fields]
    for name in device_fieldname:
        device_types = [device_type for device_type in DeviceType.__members__] 
        if name not in device_types:
            getattr(device, name)
    host = str(device.ip_address)
    port = str(device.port)
    address = host + ":" + port

    alpaca_device, context = device_chooser(device, context, address)
    try: 
        if alpaca_device.Connected:
            context["device"] = context["device"] | {
                    "connected" : alpaca_device.Connected,
                    "description" : alpaca_device.Description,
                    "driverinfo" : alpaca_device.DriverInfo,
                    "interfaceversion" : alpaca_device.InterfaceVersion,
                    "name" : alpaca_device.Name,
                    "supportedactions" : alpaca_device.SupportedActions,
                    }

        else:
            context["device"] = context["device"] | { "connected" : "False" }

    except ( AlpacaRequestException, ConnectTimeout ) as e:
        context["device"] = context["device"] | { "connected" : "False" }

    return alpaca_device, context

def device_chooser(device, context, address):
    device_type = device.devicetype.lower()
    if hasattr(DeviceType, device_type):
        if DeviceType[device_type] == DeviceType['camera']:
            alpaca_device = Camera(address, 0)
            
            context["device"] = context["device"] | {
                    "connected" : alpaca_device.Connected,
                    "camerastate" : alpaca_device.CameraState,
                            }

        elif DeviceType[device_type] == DeviceType['telescope']:
            alpaca_device = Telescope(address, 0)
            
            context["device"] = context["device"] | {
                    "name" : "telescope",
                    }
        else:
            alpaca_device = Devicebase(address, "custom", 0, "http")
            
            context["device"] = context["device"] | {
                    "name" : "Not Implemented",
                    }

    else:
        alpaca_device = Devicebase(address, "custom", 0, "http")
        context["device"] = context["device"] | {
                "name" : "Not Implemented",
                }

    return alpaca_device, context

def stop_polling(request, device_id):
    #return HttpResponse(status=286, reason="Stop Polling")
    device = Device.objects.get(pk=device_id)
    context = {"device_id": device_id}
    return render(request, "controllers/fragments/device_disconnected.html", context)

class DeviceType(Enum):
    camera          =       1
    covercalibrator =       2
    dome            =       3
    filterwheel     =       4
    focuser         =       5
    observingconditions =   6
    rotator         =       7
    safetymonitor   =       8
    switch          =       9
    telescope       =       10


