from plugins import Plugin
from .urls import urlpatterns
from .forms import form

class PPMSPlugin(Plugin):
    ID = 'ppms'
    SUBMISSION_URLS = urlpatterns
    FORM = form