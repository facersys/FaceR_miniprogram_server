# -*- coding: utf-8 -*-

from qiniu import Auth, put_data

from apps.security import QINIU_DOMAIN


class MyQiNiu:
    """
    封装七牛
    """

    def __init__(self, access_key, secret_key, bucket_name, domain):
        # 构建鉴权对象
        self.q = Auth(access_key, secret_key)
        self.bucket_name = bucket_name
        self.domain = domain

    def upload_file(self, remote_filename, data, bucket_name=None):
        """
        上传文件
        :param bucket_name: bucket名
        :param remote_filename: 远程文件名
        :param data: 文件流
        :return: 返回结果，见七牛API
        """
        bucket_name = bucket_name if bucket_name else self.bucket_name
        token = self.q.upload_token(bucket_name, remote_filename, expires=3600)

        ret, info = put_data(token, remote_filename, data)
        return self.domain + remote_filename

    def get_file(self, remote_filename):
        """下载文件"""
        # return self.q.private_download_url(QINIU_DOMAIN + remote_filename, expires=3600)
        return remote_filename
