"""
/challenges URL Configuration
"""
from django.urls import path
from .views import add_image, add_post, update_image, update_post

urlpatterns = [
    path('add_image/<str:id>', add_image, name='add_image'),
    path('add_post/<str:id>/', add_post, name='add_post'),
    path('update_image/<str:id>', update_image, name='update_image'),
    path('update_post/<str:id>/', update_post, name='update_post'),
]
