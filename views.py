from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import exceptions
from plugins import plugin_submission_decorator
from . import api
import csv

# Create your views here.
@api_view(['GET'])
@plugin_submission_decorator(permissions=['VIEW'], all=True)
def get_services(request, submission, plugin):
    response = api.post_data(plugin.settings, {"action":"getservices"})
    lines = [l.decode('utf-8') for l in response.readlines()]
    services = csv.DictReader(lines)
    return Response({'submission':submission.id, 'services': services})

@api_view(['POST'])
@plugin_submission_decorator(permissions=['STAFF'], all=True)
def create_order(request, submission, plugin):
    if 'orders' in plugin.data:
        pass
        # raise exceptions.NotAcceptable('Submission already has an order')
    else:
        plugin.data['orders'] = []
    data = {
        "action":"createorder",
        "login": request.data["username"], 
        "serviceid": request.data["serviceid"], 
        "quantity": request.data["quantity"], 
        "Scomments": "Created for submission "+submission.get_absolute_url(True)
        # "comments": "Created for submission "+submission.get_absolute_url(True)
        }
    try:
        order = api.post_data(plugin.settings, data).read().decode('utf-8')
        if not order.strip().isnumeric():
            raise exceptions.APIException(order)
    except Exception as e:
        raise exceptions.APIException(str(e))
    plugin.data['orders'].append(order.strip())
    plugin.save()
    return Response({'order':order,'plugin_data':plugin.data})

@api_view(['GET'])
@plugin_submission_decorator(permissions=['VIEW'], all=True)
def get_orders(request, submission, plugin):
    if 'orders' not in plugin.data:
        plugin.data['orders'] = []
    return Response(plugin.data)

@api_view(['GET'])
@plugin_submission_decorator(permissions=['ADMIN', 'STAFF'], all=False)
def get_all_orders(request, submission, plugin):
    return Response(api.get_orders(plugin.settings))