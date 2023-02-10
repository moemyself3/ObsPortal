from django.urls import path

#from .views import CalendarView
from . import views

app_name = 'scheduler'

urlpatterns = [
    path('', views.EventListView.as_view(), name='index'),
    path('add/', views.EventCreateView.as_view(), name='add-event'),
]
