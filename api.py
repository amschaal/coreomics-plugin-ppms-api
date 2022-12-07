"""
The API for PPMS is terrible and does not provide standard return codes formats.
Don't bother trying to make this pretty...
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import exceptions
from dnaorder.models import Submission
from plugins import plugin_submission_decorator
import csv
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
@plugin_submission_decorator(permissions=['VIEW'], all=True)
def get_services(request, submission):
    response = post_data(submission, {"action":"getservices"})
    lines = [l.decode('utf-8') for l in response.readlines()]
    services = csv.DictReader(lines)
    return Response({'submission':submission.id, 'services': services})

@api_view(['POST'])
@plugin_submission_decorator(permissions=['STAFF'], all=True)
def create_order(request, submission):
    plugin_data = submission.plugin_data.get('ppms',{})

    if 'orders' in plugin_data:
        pass
        # raise exceptions.NotAcceptable('Submission already has an order')
    else:
        plugin_data['orders'] = []
    try:
        response = post_data(submission, {"action":"createorder","login": request.POST.get("username"), "serviceid": request.POST.get("serviceid"), "quantity": request.POST.get("quantity"), "Scomments": "Created for submission "+submission.get_absolute_url(True)})
    except Exception as e:
        raise exceptions.NotAcceptable(str(e))
    order = response.read().decode('utf-8')
    plugin_data['orders'].append(order)
    submission.plugin_data['ppms'] = plugin_data
    submission.save()
    # lines = [l.decode('utf-8') for l in response.readlines()]
    # order = csv.DictReader(lines)
    return Response({'submission':submission.id, 'plugin_data': plugin_data})