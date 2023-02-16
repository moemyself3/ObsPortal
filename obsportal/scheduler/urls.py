from django.urls import path

from . import views

app_name = 'scheduler'

urlpatterns = [
    path('', views.EventListView.as_view(), name='index'),
    path('add/', views.EventCreateView.as_view(), name='add-event'),
    path('<int:pk>/update/', views.EventUpdateView.as_view(), name='update-event'),
    path('<int:pk>/delete/', views.EventDeleteView.as_view(), name='delete-event'),
    path('<int:pk>', views.EventDetailView.as_view(), name='detail-event'),
    path('category/add', views.CategoryCreateView.as_view(), name='add-category'),
]
