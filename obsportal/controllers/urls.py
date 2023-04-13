from django.urls import path

from . import views

app_name = 'controllers'

urlpatterns = [
    path('', views.SiteView.as_view() , name='index'),
]
