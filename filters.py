from rest_framework import filters
from django.contrib.auth.models import User
from django.db.models.query import Q

def parse_boolean(string):
    return True if str(string).lower() in ['true', '1', 'yes'] else False

class PPMSHasOrderFilter(filters.BaseFilterBackend):
    """
    Filter to whether a submission does or not have an associated PPMS order
    """
    def filter_queryset(self, request, queryset, view):
        has_order = view.request.query_params.get('ppms_has_order',None)
        if has_order is not None:
            isnull = not parse_boolean(has_order)
            return queryset.filter(plugin_data__ppms__orders__0__isnull=isnull)
        else:
            return queryset

class PPMSOrderFilter(filters.BaseFilterBackend):
    """
    Filter by PPMS orderref
    """
    def filter_queryset(self, request, queryset, view):
        order = view.request.query_params.get('ppms_order_contains',None)
        if order is not None:
            return queryset.filter(plugin_data__ppms__orders__icontains=str(order))
        else:
            return queryset

class PPMSUnpaidFilter(filters.BaseFilterBackend):
    """
    Submission has unpaid order which isnot cancelled
    """
    def filter_queryset(self, request, queryset, view):
        unpaid = view.request.query_params.get('ppms_unpaid',None)
        if unpaid is not None:
            return queryset.filter(plugin_data__ppms__order_details__contains=[{'paid':False,'cancelled':False}])
        else:
            return queryset 

# Submission.objects.filter(plugin_data__ppms__order_details__contains=[{'orderref':'31011'}])
PPMS_FILTER_CLASSES = [PPMSHasOrderFilter, PPMSOrderFilter, PPMSUnpaidFilter]