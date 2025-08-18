from django.urls import path
from . import views

urlpatterns = [
    path('scheduler/', views.scheduler_view, name='scheduler'),
    path('', views.dashboard_view, name='dashboard'),
]
