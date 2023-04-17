from django.shortcuts import render
from django.views.generic import DetailView, ListView
from devices.models import Site

# Main control window
#def index(request):
#    return render(request, "controllers/index.html")
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
