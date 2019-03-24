# -*- coding: utf-8 -*-
import requests
from flask import request

from apps.api import api
from apps.libs.wechat import wx_decrypt
from apps.libs.restful import success
from apps.security import APPID, SECRET_KEY
from apps.settings import CODE2SESSION_URL


@api.route('/wx/decrypt', methods=["POST"])
def decrypt():
    """
    解密
    :return: unionid
    """

    # get data
    app_id = APPID
    data = request.json

    session_key = data['session_key']
    encrypted_data = data['encryptedData']
    iv = data['iv']

    result = wx_decrypt(app_id, session_key, encrypted_data, iv)
    return success(data=result)


@api.route('/wx/code2session/<code>')
def code2session(code):
    """code to session"""
    response = requests.get(CODE2SESSION_URL.format(
        appid=APPID,
        secret=SECRET_KEY,
        js_code=code
    ))

    return success(response.json())
