from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import exceptions
from plugins import plugin_submission_decorator
from . import api
import csv

# Create your views here.
@api_view(['GET'])
@plugin_submission_decorator(permissions=['VIEW'], all=True)
def get_services(request, submission):
    response = api.post_data(submission.lab, {"action":"getservices"})
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
    data = {
        "action":"createorder",
        "login": request.data["username"], 
        "serviceid": request.data["serviceid"], 
        "quantity": request.data["quantity"], 
        "Scomments": "Created for submission "+submission.get_absolute_url(True)
        # "comments": "Created for submission "+submission.get_absolute_url(True)
        }
    try:
        order = api.post_data(submission.lab, data).read().decode('utf-8')
        if not order.strip().isnumeric():
            raise exceptions.APIException(order)
    except Exception as e:
        raise exceptions.APIException(str(e))
    plugin_data['orders'].append(order.strip())
    submission.plugin_data['ppms'] = plugin_data
    submission.save()
    # lines = [l.decode('utf-8') for l in response.readlines()]
    # order = csv.DictReader(lines)
    return Response({'order':order,'plugin_data':plugin_data})

@api_view(['GET'])
@plugin_submission_decorator(permissions=['VIEW'], all=True)
def get_orders(request, submission):
    # response = post_data(submission, {"action":"getservices"})
    # lines = [l.decode('utf-8') for l in response.readlines()]
    # services = csv.DictReader(lines)
    plugin_data = submission.plugin_data.get('ppms',{})
    if 'orders' not in plugin_data:
        plugin_data['orders'] = []
    return Response(plugin_data)