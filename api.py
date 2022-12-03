"""
The API for PPMS is terrible and does not provide standard return codes formats.
Don't bother trying to make this pretty...
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from dnaorder.models import Submission
# #Python 3 POST
from urllib import request, parse
def post_data(submission, params):
    params['apikey'] = submission.lab.plugins['ppms']['private']['pumapi_token']
    data = parse.urlencode(params).encode()
    req =  request.Request(submission.lab.plugins['ppms']['private']['pumapi_url'], data=data) # this will make the method "POST"
    resp = request.urlopen(req)
    return resp
# post_data({"action":"getservices"})

# @csrf_exempt
@api_view(['GET'])
@permission_classes((AllowAny,))
def get_services(request, submission_id):
    submission = Submission.objects.get(id=submission_id)
    response = post_data(submission, {"action":"getservices"})
    return Response({'response': response.read()})