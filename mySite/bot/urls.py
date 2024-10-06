from django.urls import path, include
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('',home,name = 'home'),
    path('login/',login,name = 'login'),
    path('api/get_username/',get_username,name = 'get_username'),
    path('api/raise_ticket/',raise_ticket,name = 'raise_ticket'),
    path('api/ticket_status/',ticket_status,name = 'ticket_status'),

    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
