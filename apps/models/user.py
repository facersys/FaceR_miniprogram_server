# -*- coding: utf-8 -*-

import time
from apps.libs import mongo
from apps.security import MONGO_USER_COLLECTION
from apps.settings import DEFAULT_AVATAR


class UserModel:
    """User Model
    params:
       sid: 学号
       name: 姓名
       gender: 性别
       grade: 年级
       major: 专业
       cname: 班级id
       face: 人脸编码
       face_url: 对应人脸图像的url
       created: 创建时间
       openid: 微信openid
       unionid: 微信unionid
       is_bind_jw: 是否绑定教务系统
       avatar: 头像
       city: 城市
       province: 省份
    """

    def __init__(self, **kwargs):
        self.__info = kwargs

        self.__sid = str(self.__info.get('sid', int(time.time())))
        self.__name = self.__info.get('name')
        self.__gender = self.__info.get('gender')
        self.__grade = self.__info.get('grade', 2015)
        self.__major = self.__info.get('major')
        self.__cname = self.__info.get('cname')
        self.__face = self.__info.get('face', [])
        self.__face_url = self.__info.get('face_url')
        self.__email = self.__info.get('email')

        self.__openid = self.__info.get('openid')
        self.__unionid = self.__info.get('unionid')
        self.__is_bind_jw = self.__info.get('is_bind_jw', False)
        self.__avatar = self.__info.get('avatar', DEFAULT_AVATAR)
        self.__city = self.__info.get('city')
        self.__province = self.__info.get('province')

    @property
    def get(self):
        self.__info.update({
            "_id": int(time.time()),
            "sid": self.__sid,
            "name": self.__name,
            "gender": self.__gender,
            "grade": self.__grade,
            "major": self.__major,
            "cname": self.__cname,
            "face": self.__face,
            "face_url": self.__face_url,
            "email": self.__email,

            "openid": self.__openid,
            "unionid": self.__unionid,
            "is_bind_jw": self.__is_bind_jw,
            'avatar': self.__avatar,
            'city': self.__city,
            'province': self.__province
        })
        return self.__info

    def save(self):
        """save to mongo"""
        return mongo.insert(MONGO_USER_COLLECTION, self.get, indexs=['sid', 'openid', 'unionid'])

    def __repr__(self):
        return str(self.get)
