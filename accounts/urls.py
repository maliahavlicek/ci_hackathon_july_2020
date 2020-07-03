from django.conf.urls import include
from django.urls import path
from accounts.views import logout, login, registration
from accounts import url_reset

urlpatterns = [
    path('logout/', logout, name='logout'),
    path('login/', login, name='login'),
    path('register/', registration, name='registration'),
    path('password-reset/', include(url_reset)),
]

