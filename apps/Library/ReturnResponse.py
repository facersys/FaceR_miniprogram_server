# -*- coding: utf-8 -*-
import json

from flask import Response


class ReturnResponse:
    def __init__(self, code, data, detail):
        response = Response(json.dumps(data), mimetype='application/json')
        response.headers.add('Server', 'python flask')
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
        response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
