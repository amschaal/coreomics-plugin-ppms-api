from plugins import Plugin
from .urls import urlpatterns
from .forms import form
from .serializers import PPMSPaymentType
from . import filters
class PPMSPlugin(Plugin):
    ID = 'ppms'
    SUBMISSION_URLS = urlpatterns
    FORM = form
    PAYMENT = PPMSPaymentType
    FILTERS = {
        'ppms_has_order': { "type": "boolean", "title": "Has PPMS Order", "enum": ['True', 'False'], "filters": [{"label": "=", "filter": "ppms_has_order"}]},
        'ppms_order': { "type": "string", "title": "PPMS Order Ref", "filters": [{"label": "Order Ref Contains", "filter": "ppms_order_contains"}]},
    }
    FILTER_CLASSES = filters.PPMS_FILTER_CLASSES