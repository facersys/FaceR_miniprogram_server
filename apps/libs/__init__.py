# -*- coding: utf-8 -*-
from aip import AipOcr

from apps.libs.mongo import MongoTools
from apps.libs.mtcnn.mtcnn import MTCNN
from apps.libs.qiniu import MyQiNiu
from apps.security import MONGO_DATABASE, QINIU_ACCESS_KEY, \
    QINIU_SECRET_KEY, QINIU_BUCKET_NAME, QINIU_DOMAIN, \
    BD_APP_ID, BD_API_KEY, BD_SECRET_KEY

mongo = MongoTools(MONGO_DATABASE)
qiniu = MyQiNiu(
    access_key=QINIU_ACCESS_KEY,
    secret_key=QINIU_SECRET_KEY,
    bucket_name=QINIU_BUCKET_NAME,
    domain=QINIU_DOMAIN
)
aipOcr = AipOcr(BD_APP_ID, BD_API_KEY, BD_SECRET_KEY)
