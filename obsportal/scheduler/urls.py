from django.urls import path

#from .views import CalendarView
from . import views

app_name = 'scheduler'

urlpatterns = [
    path('', views.CalendarView, name='index'),
    path('add/', views.EventCreateView.as_view(), name='add-event'),
]
