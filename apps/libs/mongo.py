# -*- coding: utf-8 -*-

import pymongo
from apps.security import MONGO_URI

__author__ = "YingJoy"


class MongoTools:

    def __init__(self, db):
        """
        初始化
        """
        self.mongo_client = pymongo.MongoClient(MONGO_URI)
        self.db = self.mongo_client[db]

    def insert(self, collection, document, indexs=None):
        """
        插入文档
        :param document: 文档
        :param collection: collection
        :param indexs: 索引（可选）
        :return: 是否插入成功
        """
        c = self.db[collection]
        if indexs:
            """指定索引"""
            for index in indexs:
                c.create_index([(index, pymongo.ASCENDING)], unique=True)

        # 判断插入数据是否成功
        try:
            return True if c.insert(document) else False
        except Exception as e:
            print(e)
            return False

    def find(self, collection, item=None):
        """
        查询所有
        :param collection: collection
        :param item: 条件
        :return:
        """
        return self.db[collection].find(item)

    def do(self, collection):
        """使用原生pymongo"""
        return self.db[collection]

    def select_one(self, collection, item):
        """
        查询一条文档
        :param collection: 集合
        :param item: 查询要求
        :return: 文档
        """
        document = self.db[collection].find_one(item)
        return document

    def update(self, collection, item, update_kvs):
        """
        更新一条文档
        :param collection: collection
        :param item: 查询要求
        :param update_kvs: 更新后的值
        :return: Boolean
        """
        c = self.db[collection]
        try:
            c.update(item, {"$set": update_kvs})
            return True
        except Exception as e:
            print(e)
            return False

    def delete(self, collection, item):
        """
        删除文档
        :param collection:
        :param item:
        :return:
        """
        return self.db[collection].delete_one(item)

