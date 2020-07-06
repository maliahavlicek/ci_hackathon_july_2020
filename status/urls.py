"""
/ratings URL Configuration
"""
from django.urls import path
from .views import SendStatus

urlpatterns = [
    path('send_status/', SendStatus.as_view(), name='send_status'),
]
