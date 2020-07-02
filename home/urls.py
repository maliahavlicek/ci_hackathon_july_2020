"""
/home URL Configuration
"""
from django.urls import path
from .views import index, http404, http500

from django.conf import settings

urlpatterns = [
    path('', index, name='index'),

]

if settings.DEBUG:
    urlpatterns = [
        path("404", http404),
        path("500", http500),
    ] + urlpatterns
