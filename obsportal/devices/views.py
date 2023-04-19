import ast

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import CreateView, DeleteView, FormView, UpdateView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.forms import formset_factory, modelformset_factory

from .forms import DiscoveryForm, RegisterDeviceForm, AddSiteForm, SiteDeviceFormset
from .models import Device, Site

### Site views ###
class SiteListView(ListView):
    model = Site
    template_name = 'devices/sites.html'
    context_object_name = 'site_list'

class SiteCreateView(SuccessMessageMixin, CreateView):
    template_name = 'devices/addsite.html'
    form_class = AddSiteForm
    success_message = "%(name)s was created successfully"
    
class SiteDetailView(DetailView):
    model = Site
    template_name = 'devices/site_detail.html'

class SiteDeleteView(SuccessMessageMixin, DeleteView):
    model = Site
    template_name = 'devices/deletesite.html'
    success_message = "Site was deleted successfully"
    success_url = reverse_lazy('devices:sites')

class SiteUpdateView(SuccessMessageMixin, UpdateView):
    model = Site
    form_class = AddSiteForm
    template_name = 'devices/updatesite.html'
    success_message = "%(name)s was updated successfully"

### Device views ###
class IndexView(ListView):
    template_name = 'devices/index.html'
    context_object_name = 'device_list'

    def get_queryset(self):
        """Return list of registered devices."""
        return Device.objects.all()

class DeviceDetailView(DetailView):
    context_object_name = 'device'
    model = Device
    template_name = 'devices/device_detail.html'

class DeviceCreateView(SuccessMessageMixin, CreateView):
    template_name = 'devices/adddevice.html'
    form_class = RegisterDeviceForm
    success_message = "%(devicename)s was created successfully"
#    success_url = reverse_lazy('devices:index')

class DeviceDeleteView(SuccessMessageMixin, DeleteView):
    model = Device
    template_name = 'devices/deletedevice.html'
    success_message = "Device was deleted successfully"
    success_url = reverse_lazy('devices:index')

class DeviceUpdateView(SuccessMessageMixin, UpdateView):
    model = Device
    form_class = RegisterDeviceForm
    template_name = 'devices/updatedevice.html'
    success_message = "%(devicename)s was updated successfully"

## Cross Site Device View
# TODO: Class Based View of transfer
class AlpacaSiteDevicesView(SingleObjectMixin, FormView):
    model = Site
    template_name = 'devices/updatesitedevices.html'
    form_class = RegisterDeviceForm

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Site.objects.all())
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Site.objects.all())
        return super().post(request, *args, **kwargs)

    def get_form(self, form_class=RegisterDeviceForm):
        return SiteDeviceFormset(**self.get_form_kwargs(), instance=self.object)

    def form_valid(self, form):
        form.save()
        messages.add_message(
                self.request,
                messages.SUCCESS,
                'Changes were saved.'
                )
        return HttpResponseRedirect(self.get_success_url())
    
    def get_success_url(self):
        return reverse('devices:site-detail', kwargs={'pk': self.object.pk})
 
# Function based view of transfer
def alpaca_registration_site_transfer(request):

    if request.method == "POST":
        DeviceModel = Device
        site = []
        site = request.POST.getlist('site')
        selected = request.POST.getlist('selected')
        device_quantity = len(selected)
        device_data = []
        if selected==[]:
            messages.add_message(
                request,
                messages.WARNING,
                'Nothing was selected. Nothing was added.'
                )
            return HttpResponseRedirect(reverse('devices:site-detail', kwargs={'pk':site[0]}))

        for index, device_info in enumerate(selected):
            device_info = ast.literal_eval(device_info)
            device_info = alpaca_discovery_to_form(device_info)
            device_info['site'] = site
            device_data.append(device_info)
        
        RegisterDeviceFormset = modelformset_factory(
                                                Device,
                                                form=RegisterDeviceForm,
                                                min_num=device_quantity,
                                                extra=0
                                                )

        formset = RegisterDeviceFormset(initial=device_data, queryset=Device.objects.none())
        return render(request, 'devices/alpacatransfer.html', {'formset':formset, 'site':site, 'selected':selected})
    else:
        return render(request, 'devices/alpacatransfer.html')

def save_alpaca_registration(request):
    RegisterDeviceFormset = modelformset_factory(Device, form=RegisterDeviceForm)
    if request.method == "POST":
        formset = RegisterDeviceFormset(request.POST, queryset=Device.objects.none())
        if formset.is_valid():
            for form in formset:
                print(form)
                form.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                'Changes were saved.'
                )
            return HttpResponseRedirect(reverse('devices:site-detail', kwargs={'pk':request.POST['form-0-site']}))
        else:
            return render(request, 'devices/alpacatransfer.html')
    else:
        return render(request, 'devices/alpacatransfer.html')

# Helper function to translate dicovery dictionary output to form
def alpaca_discovery_to_form(device_data):
    device_data= {key.lower(): value for key, value in device_data.items()}
    device_data['ip_address'], device_data['port'] = device_data.pop('serveraddress').split(':')
    device_data['description'] = 'Device Number' + str(device_data.pop('devicenumber')) + ' Unique ID: ' + device_data.pop('uniqueid')
    device_data['supportedactions']={'':''}
    device_data['driverinfo']='update'
    device_data['driverversion']=0
    device_data['interfaceversion']=0
    return device_data

class UpdateSiteDevicesView(SingleObjectMixin, FormView):
    model = Site
    template_name = 'devices/updatesitedevices.html'
    form_class = RegisterDeviceForm

    if Site.objects.exists():
        def get(self, request, *args, **kwargs):
            self.object = self.get_object(queryset=Site.objects.all())
            return super().get(request, *args, **kwargs)
    
        def post(self, request, *args, **kwargs):
            self.object = self.get_object(queryset=Site.objects.all())
            return super().post(request, *args, **kwargs)
    
        def get_form(self, form_class=RegisterDeviceForm):
            return SiteDeviceFormset(**self.get_form_kwargs(), instance=self.object)
    
        def form_valid(self, form):
            form.save()
            messages.add_message(
                    self.request,
                    messages.SUCCESS,
                    'Changes were saved.'
                    )
            return HttpResponseRedirect(self.get_success_url())
        
        def get_success_url(self):
            return reverse('devices:site-detail', kwargs={'pk': self.object.pk})
    
    else:
        # if no site exists then redirect to `devices:add-site` with a message
        def redirect(self, request, *args, **kwargs):
            messages.add_message(
                    self.request,
                    messages.WARNING,
                    'No site exists. Please setup a site first.')

            return HttpResponseRedirect(reverse('devices:add-site'))

        def get(self, request, *args, **kwargs):
            return self.redirect(self, request, *args, **kwargs)

        def post(self, request, *args, **kwargs):
            return self.redirect(self, request, *args, **kwargs)

class AlpacaDiscoveryView(FormView):
    template_name = 'devices/alpacadiscovery.html'
    form_class = DiscoveryForm
    success_url = 'alpacadiscovery'

    def form_valid(self, form):
        if not Site.objects.exists():
            messages.add_message(
                    self.request, 
                    messages.WARNING, 
                    'No site exists. You can still use Discovery, but you need to add a site before being able to register devices.')
        
        sites = Site.objects.all()
        
        devices = {'devices':form.alpaca_discovery(), 'form':form, 'sites': sites}
        return render(self.request, self.template_name, devices)
