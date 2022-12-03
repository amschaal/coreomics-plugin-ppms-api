from django.urls import include, path
from . import api

urlpatterns = [
    path('services/', api.get_services, name='ppms_services')
]