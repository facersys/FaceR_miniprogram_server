# -*- coding: utf-8 -*-

import json
import base64

from Crypto.Cipher import AES


class WXBizDataCrypt:
    def __init__(self, appId, sessionKey):
        self.appId = appId
        self.sessionKey = sessionKey

    def decrypt(self, encryptedData, iv):
        # base64 decode
        sessionKey = base64.b64decode(self.sessionKey)
        encryptedData = base64.b64decode(encryptedData)
        iv = base64.standard_b64decode(iv)

        cipher = AES.new(sessionKey, AES.MODE_CBC, iv)
        decrypted = json.loads(self._unpad(cipher.decrypt(encryptedData)))

        if decrypted['watermark']['appid'] != self.appId:
            raise Exception('Invalid Buffer')

        return decrypted

    def _unpad(self, s):
        print('-' * 20)
        print(s)
        print('-' * 20)
        return s[:-ord(s[len(s)-1:])]


def wx_decrypt(app_id, session_key, encrypted_data, iv):
    """解密"""
    pc = WXBizDataCrypt(app_id, session_key)
    return pc.decrypt(encrypted_data, iv)

