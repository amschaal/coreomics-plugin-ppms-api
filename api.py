"""
The API for PPMS is terrible and does not provide standard return codes formats.
Don't bother trying to make this pretty...
"""

import csv
# #Python 3 POST
from urllib import request, parse
def post_data(settings, params):
    params['apikey'] = settings['pumapi_token']
    data = parse.urlencode(params).encode()
    req =  request.Request(settings['pumapi_url'], data=data) # this will make the method "POST"
    resp = request.urlopen(req)
    return resp

def group_exists(settings, unitlogin):
    response = post_data(settings, {"action":"getgroup","unitlogin":unitlogin})
    lines = [l.decode('utf-8') for l in response.readlines()]
    if len(lines) > 1:
        return True
    return False

def get_orders(settings):
    response = post_data(settings, {"action":"getorders"})
    lines = [l.decode('utf-8') for l in response.readlines()]
    return list(csv.DictReader(lines[1:]))