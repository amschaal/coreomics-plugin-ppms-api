from django.urls import include, path
from . import api

urlpatterns = [
    path('services/', api.get_services, name='ppms_services'),
    path('create_order/', api.create_order, name='create_order')
]