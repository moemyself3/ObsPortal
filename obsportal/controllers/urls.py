from django.urls import path

from . import views

app_name = 'controllers'

urlpatterns = [
    path('', views.IndexView.as_view() , name='index'),
    path('site/<int:pk>', views.SiteDetailView.as_view(), name='site-detail'),
    path('telescopedemo', views.TelescopeDemoView, name='telescope-demo'),
]
