from django.conf.urls import url, include
from django.urls import path
from accounts.views import index, logout, login, registration, user_profile
from accounts import url_reset

urlpatterns = [
    path('logout/', logout, name='logout'),
    # url(r'^logout/$', logout, name='logout'),
    url(r'^login/$', login, name='login'),
    path('register/', registration, name='registration'),
    # url(r'^register/$', registration, name='registration'),
    path('profile/', user_profile, name='profile'),
    # url(r'^profile/$', user_profile, name='profile'),
    path('password-reset/', include(url_reset))
   #  url(r'^password-reset/', include(url_reset))
]

