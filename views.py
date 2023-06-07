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

@api_view(['GET'])
@plugin_submission_decorator(permissions=['ADMIN', 'STAFF'], all=False)
def get_user_info(request, submission, plugin):
    emails = set([submission.email, submission.pi_email])
    accounts = []
    for email in emails:
        accounts += api.get_user_info(plugin.settings, email)
    # accounts = { email: api.get_user_info(plugin.settings, email) for email in emails }
    return Response(accounts)

@api_view(['GET'])
@plugin_submission_decorator(permissions=['ADMIN', 'STAFF'], all=False)
def search_orders(request, submission, plugin):
    comment = request.query_params.get('comment','')
    order_ids = request.query_params.getlist('order_ids[]',[])
    date_gte = request.query_params.get('date_gte','')
    if not comment and not order_ids and not date_gte:
        raise exceptions.NotAcceptable('Please provide a query for at least one of the following: comment, order_ids, date_gte')
    orders = api.search_orders(plugin.settings, comment=comment, unit_id=request.GET.get('unit_id',0), order_ids=order_ids, date_gte=date_gte)
    return Response(orders)

@api_view(['POST'])
@plugin_submission_decorator(permissions=['ADMIN', 'STAFF'], all=False)
def import_order(request, submission, plugin):
    order_id = request.data.get('order_id')
    orders = api.search_orders(plugin.settings, order_ids=[order_id])
    if not orders:
        raise exceptions.NotAcceptable('Unable to find order {}'.format(order_id))
    if 'orders' not in plugin.data:
        plugin.data['orders'] = []
    plugin.data['orders'].append(order_id)
    plugin.save()
    return Response(orders)
