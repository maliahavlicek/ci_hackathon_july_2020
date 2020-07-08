"""
/ratings URL Configuration
"""
from django.urls import path
from .views import SendStatus, GetAllStatus

urlpatterns = [
    path('send_status/', SendStatus.as_view(), name='send_status'),
    path('get_status/', GetAllStatus.as_view(), name='get_status'),
]
