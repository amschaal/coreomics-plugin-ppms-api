from rest_framework import filters
from django.contrib.auth.models import User
from django.db.models.query import Q

class PPMSHasOrderFilter(filters.BaseFilterBackend):
    """
    Filter to whether a submission does or not have an associated PPMS order
    """
    def filter_queryset(self, request, queryset, view):
        has_order = view.request.query_params.get('ppms_has_order',None)
        if has_order is not None:
            if str(has_order).lower() in ['true', '1', 'yes']:
                isnull = False
            else:
                isnull = True
            return queryset.filter(plugin_data__ppms__orders__0__isnull=isnull)
        else:
            return queryset

PPMS_FILTER_CLASSES = [PPMSHasOrderFilter]