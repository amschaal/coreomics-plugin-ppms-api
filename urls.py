from django.urls import include, path
from . import views

urlpatterns = [
    path('services/', views.get_services, name='ppms_services'),
    path('orders/', views.get_orders, name='ppms_submission_orders'),
    path('all_orders/', views.get_all_orders, name='ppms_all_orders'),
    path('create_order/', views.create_order, name='ppms_create_order'),
    path('user_info/', views.get_user_info, name='ppms_user_info'),
    path('search_orders/', views.search_orders, name='ppms_search_orders'),
    path('import_order/', views.import_order, name='ppms_import_order')
]