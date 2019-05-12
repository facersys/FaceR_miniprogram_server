# -*- coding: utf-8 -*-

OK = 0  # 正常

NOTICE_LOST_PARAM = 71  # 通知接口缺少参数

USER_NOT_FOUND = 80  # 用户未找到
USERID_LOST = 81  # 未传入用户ID
USER_EXISTS = 82  # 用户已存在
JW_LOST_PARAM = 83  # 绑定教务系统缺少参数
JW_ACCOUNT_ERROR = 84  # 教务系统账户或密码错误
JW_FAILURE = 85  # 绑定教务系统失败

NOTICE_NOT_FOUND = 90  # 通知不存在
NOTICEID_LOST = 91  # 未传入通知ID

WECHAT_DECRYPT_LOST_PARAM = 401  # 微信解密缺少参数

UNKNOWN_ERROR = 407  # 未知错误
SERVER_ERROR = 500  # 服务器异常
NETWORK_ERROR = 501  # 网络错误
