from django.urls import path

from . import views

app_name = 'controllers'

urlpatterns = [
    path('', views.IndexView.as_view() , name='index'),
    path('site/<int:pk>', views.SiteDetailView.as_view(), name='site-detail'),
    path('telescopedemo', views.TelescopeDemoView, name='telescope-demo'),
    path('device/<int:device_id>', views.DeviceView, name='device'),
    path('device/<int:device_id>/stop', views.stop_polling, name='stop'),
]
