"""
The API for PPMS is terrible and does not provide standard return codes formats.
Don't bother trying to make this pretty...
"""

import csv
# #Python 3 POST
from urllib import request, parse
def post_data(lab, params):
    params['apikey'] = lab.plugins['ppms']['private']['pumapi_token']
    data = parse.urlencode(params).encode()
    req =  request.Request(lab.plugins['ppms']['private']['pumapi_url'], data=data) # this will make the method "POST"
    resp = request.urlopen(req)
    return resp

def group_exists(lab, unitlogin):
    response = post_data(lab, {"action":"getgroup","unitlogin":unitlogin})
    lines = [l.decode('utf-8') for l in response.readlines()]
    # data = response.read().decode('utf-8')
    # if len(data.split('\n')) > 1:
    #     return True
    if len(lines) > 1:
        return True
    return False

def get_orders(lab, unitlogin):
    response = post_data(lab, {"action":"getorders","unitlogin":unitlogin})
    lines = [l.decode('utf-8') for l in response.readlines()]
    return list(csv.DictReader(lines[1:]))