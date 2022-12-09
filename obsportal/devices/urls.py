from django.urls import path

from . import views

app_name = 'devices'
urlpatterns = [
        path('', views.IndexView.as_view(), name='index'),
        path('alpacadiscovery/', views.AlpacaDiscoveryView.as_view(), name='alpaca-discovery'),
        path('add/', views.DeviceCreateView.as_view(), name='add-device'),
        path('<int:pk>/', views.DeviceDetailView.as_view(), name='device-detail'),
        path('<int:pk>/update/', views.DeviceUpdateView.as_view(), name='update-device'),
        path('<int:pk>/delete/', views.DeviceDeleteView.as_view(), name='delete-device'),
        path('sites/<int:pk>/updatesitedevices', views.UpdateSiteDevicesView.as_view(), name='update-site-devices'),
        path('sites/', views.SiteListView.as_view(), name='sites'),
        path('sites/add/', views.SiteCreateView.as_view(), name='add-site'),
        path('sites/<int:pk>/', views.SiteDetailView.as_view(), name='site-detail'),
        path('sites/<int:pk>/update/', views.SiteUpdateView.as_view(), name='update-site'),
        path('sites/<int:pk>/delete/', views.SiteDeleteView.as_view(), name='delete-site'),
        path('alpacatransfer/', views.alpaca_registration_site_transfer, name='alpaca-transfer'),
        path('alpacatransfer/registration/', views.save_alpaca_registration, name='alpaca-registration'),
]
