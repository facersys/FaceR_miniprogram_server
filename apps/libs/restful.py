# -*- coding: utf-8 -*-

from flask import jsonify


class HttpCode(object):
    """Http状态码"""
    ok = 200
    not_found = 404
    params_error = 400
    server_error = 500


def restful_result(code, data=None, message=None):
    return jsonify({
        "code": code,
        "message": message,
        "data": data
    })


def success(data=None, message=None):
    """成功"""
    return restful_result(HttpCode.ok, data=data, message=message)


def params_error(message=None):
    """参数错误"""
    return restful_result(code=HttpCode.params_error, message=message)


def server_error(message=None):
    """服务器错误"""
    return restful_result(code=HttpCode.server_error, message=message or "服务器内部错误")
