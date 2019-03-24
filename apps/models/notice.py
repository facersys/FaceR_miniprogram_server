# -*- coding: utf-8 -*-

import time

from apps.libs import mongo
from apps.security import MONGO_NOTICE_COLLECTION


class NoticeModel:
    """Notice Model
    params:
        sid: 用户id
        title: 标题
        content: 内容
        created: 创建时间
        is_read: 是否已读 (否)
    """

    def __init__(self, sid, title, content):
        self.__sid = sid
        self.__title = title
        self.__content = content
        self.__is_read = False

    @property
    def get(self):
        return {
            "_id": int(time.time()),
            "sid": self.__sid,
            "title": self.__title,
            "content": self.__content,
            "is_read": self.__is_read
        }

    def save(self):
        return mongo.insert(MONGO_NOTICE_COLLECTION, self.get)

    def __repr__(self):
        return str(self.get)
