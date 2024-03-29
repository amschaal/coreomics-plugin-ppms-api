"""
The API for PPMS is terrible and does not provide standard return codes formats.
Don't bother trying to make this pretty...
"""

import csv, json
# #Python 3 POST
from urllib import request, parse

def get_lab_settings(lab):
    from .plugin import PPMSPlugin
    return lab.get_plugin_settings_by_id(PPMSPlugin.ID, private=True, institution=True)

def post_data(settings, params, api2=False):
    url = '{}/{}/'.format(settings['ppms_url'], 'API2' if api2 else 'pumapi')
    params['apikey'] = settings['api2_token'] if api2 else settings['pumapi_token']
    data = parse.urlencode(params).encode()
    # print(url, data)
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
    response = post_data(settings, {"action":settings.get('user_info_report_id','Report2168'),"email":email,"outformat":"json"},api2=True)
    body = response.read()
    if not body:
        return []
    return json.loads(body)

def search_orders(settings, comment='', unit_id=0, order_ids=[], date_gte=''):
    response = post_data(settings, {"action":settings.get('order_search_report_id','Report2167'),"coreid": settings.get("core_id"),"comment_contains":comment, "unitID":unit_id, "order_refs": ','.join(order_ids), "date_gte":date_gte,"outformat":"json"},api2=True)
    body = response.read()
    if not body:
        return []
    orders = json.loads(body)
    orders_dict = {}
    for o in orders:
        if o['orderref'] in orders_dict:
            if o['staff_comment']:
                orders_dict[o['orderref']]['staff_comment'] += ', ' + o['staff_comment']
        else:
            orders_dict[o['orderref']] = o
    return list(orders_dict.values())

def get_orders(settings):
    response = post_data(settings, {"action":"getorders"})
    lines = [l.decode('utf-8') for l in response.readlines()]
    return list(csv.DictReader(lines[1:]))