# -*- coding: utf-8 -*-

SERVER_NAME = "facer.yingjoy.cn"

# File Config
FILE_ALLOWED = ['image/png', 'image/jpg', 'image/jpeg']

# URLs
CODE2SESSION_URL = "https://api.weixin.qq.com/sns/jscode2session?appid={appid}" \
                   "&secret={secret}&js_code={js_code}&grant_type=authorization_code"

DEFAULT_AVATAR = "https://facer.yingjoy.cn/static/logo.png"
