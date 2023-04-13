from django.shortcuts import render
from django.views.generic import ListView
from devices.models import Site

# Main control window
#def index(request):
#    return render(request, "controllers/index.html")

class SiteView(ListView):
    model = Site
    template_name = 'controllers/index.html'
    context_object_name = 'sites'
    
