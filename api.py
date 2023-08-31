"""
The API for PPMS is terrible and does not provide standard return codes formats.
Don't bother trying to make this pretty...
"""

import csv, json
# #Python 3 POST
from urllib import request, parse

def get_lab_settings(lab):
    from .plugin import PPMSPlugin
    return lab.get_plugin_settings(private=True).get(PPMSPlugin.ID, {})

def post_data(settings, params, api2=False):
    url = '{}/{}/'.format(settings['ppms_url'], 'API2' if api2 else 'pumapi')
    params['apikey'] = settings['api2_token'] if api2 else settings['pumapi_token']
    data = parse.urlencode(params).encode()
    req =  request.Request(url, data=data) # this will make the method "POST"
    resp = request.urlopen(req)
    return resp

def get_group(settings, unitlogin):
    response = post_data(settings, {"action":"getgroup","unitlogin":unitlogin})
    lines = [l.decode('utf-8') for l in response.readlines()]
    if len(lines) > 1:
        return list(csv.DictReader(lines))
    return None

def group_exists(settings, unitlogin):
    response = post_data(settings, {"action":"getgroup","unitlogin":unitlogin})
    lines = [l.decode('utf-8') for l in response.readlines()]
    if len(lines) > 1:
        return True
    return False

def get_user_info(settings, email):
    response = post_data(settings, {"action":"Report2168","email":email,"outformat":"json"},api2=True)
    body = response.read()
    if not body:
        return []
    return json.loads(body)

def search_orders(settings, comment='', unit_id=0, order_ids=[], date_gte=''):
    response = post_data(settings, {"action":"Report2167","comment_contains":comment, "unitID":unit_id, "order_refs": ','.join(order_ids), "date_gte":date_gte,"outformat":"json"},api2=True)
    body = response.read()
    if not body:
        return []
    return json.loads(body)

def get_orders(settings):
    response = post_data(settings, {"action":"getorders"})
    lines = [l.decode('utf-8') for l in response.readlines()]
    return list(csv.DictReader(lines[1:]))