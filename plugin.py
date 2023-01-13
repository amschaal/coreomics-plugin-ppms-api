from plugins import Plugin
from .urls import urlpatterns
from .forms import form
from .serializers import PPMSPaymentType

class PPMSPlugin(Plugin):
    ID = 'ppms'
    SUBMISSION_URLS = urlpatterns
    FORM = form
    PAYMENT = PPMSPaymentType