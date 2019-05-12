# -*- coding: utf-8 -*-

import json
from flask import Response

from apps.Library.ReturnStatus import OK, UNKNOWN_ERROR


def _Return_Post(data, message=None, code=OK, **kwargs):
    """
    用户反馈响应
    """
    response = Response(json.dumps({
        "code": code,
        "data": data,
        "message": message,
        "others": kwargs
    }), mimetype='application/json')
    response.headers.add('Server', 'python flask')
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
    return response


def _Return_Error_Post(data=None, message=None, code=UNKNOWN_ERROR, **kwargs):
    """
    用于反馈错误响应
    """
    response = Response(json.dumps({
        "code": code,
        "data": data,
        "message": message,
        "others": kwargs
    }), mimetype='application/json')
    response.headers.add('Server', 'python flask')
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
    return response
