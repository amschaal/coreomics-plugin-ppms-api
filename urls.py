from django.urls import include, path
from . import views

urlpatterns = [
    path('services/', views.get_services, name='ppms_services'),
    path('orders/', views.get_orders, name='ppms_submission_orders'),
    path('create_order/', views.create_order, name='create_order')
]