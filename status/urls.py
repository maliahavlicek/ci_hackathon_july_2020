"""
/ratings URL Configuration
"""
from django.urls import path
from .views import send_status, get_all_status

urlpatterns = [
    path('send_status', send_status, name='send_status'),
    path('get_all_status', get_all_status, name='get_all_status'),
]
