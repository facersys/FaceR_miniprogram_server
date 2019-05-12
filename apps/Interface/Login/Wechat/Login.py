# -*- coding: utf-8 -*-

import requests
from flask import request

from apps.Interface import api
from apps.Library import log
from apps.Library.ReturnResponse import _Return_Post, _Return_Error_Post
from apps.Library.ReturnStatus import OK, WECHAT_DECRYPT_LOST_PARAM, NETWORK_ERROR
from apps.Library.WechatTools import wx_decrypt
from apps.Config import getConfig
from apps.Config.APIs import CODE2SESSION_URL


@api.route('/test')
def api_test():
    log.logger.debug("请求测试服务器是否正常工作")
    return _Return_Post(data=[], detail='测试请求成功', code=OK)


@api.route('/wx/decrypt', methods=["POST"])
def decrypt():
    """
    解密微信反馈的信息
    session_key, encrypted_data, iv 必需
    :return: unionid
    """

    data = request.json or {}

    session_key = data.get('session_key', None)
    encrypted_data = data.get('encryptedData', None)
    iv = data.get('iv', None)

    # 缺少参数
    if not bool(session_key and encrypted_data and iv):
        log.logger.warning("微信解密信息缺少参数")
        return _Return_Error_Post(code=WECHAT_DECRYPT_LOST_PARAM, message="微信解密信息缺少参数")

    result = wx_decrypt(
        getConfig("wechat", "appid"),
        session_key,
        encrypted_data,
        iv
    )

    log.logger.info('解密微信信息成功: ' + result)
    return _Return_Post(data=result, message='微信解密信息成功')


@api.route('/wx/code2session/<code>')
def code2session(code):
    """
    code to session
    """
    try:
        response = requests.get(CODE2SESSION_URL.format(
            appid=getConfig("wechat", "appid"),
            secret=getConfig("wechat", "secret_key"),
            js_code=code
        ))
    except:
        log.logger.warning("网络错误")
        return _Return_Error_Post(code=NETWORK_ERROR, message='网络错误')

    log.logger.info('微信code2session成功: ' + response.json())
    return _Return_Post(data=response.json(), message='微信code2session成功')
