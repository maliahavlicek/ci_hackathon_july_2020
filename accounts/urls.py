from django.conf.urls import include
from django.urls import path
from accounts.views import logout, login, registration, create_family, wall, default_wall
from accounts import url_reset

urlpatterns = [
    path('logout/', logout, name='logout'),
    path('login/', login, name='login'),
    path('register/', registration, name='registration'),
    path('password-reset/', include(url_reset)),
    path('create_family/', create_family, name='create_family'),
    path('wall/', default_wall, name='default_wall'),
    path('get_family/<str:id>/', wall, name='wall'),
]
