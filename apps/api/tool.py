# -*- coding: utf-8 -*-

import time

from flask import request
from apps.api import api
from apps.libs import qiniu, mongo
from apps.libs.face import FaceTool
from apps.libs.restful import params_error, success
from apps.security import MONGO_USER_COLLECTION


@api.route('/face', methods=["POST"])
def face():
    face_stream = request.files.get('face').read()
    face_code = FaceTool(face_stream)
    print(face_code.encode())
    return "face"


@api.route('/upload_face', methods=["POST"])
def upload_face():
    oid = request.form.get('oid')

    user = mongo.select_one(MONGO_USER_COLLECTION, {'openid': oid})
    if not user:
        return params_error(message='用户不存在')
    filename = "{}-{}-{}-face.png".format(str(int(time.time())), user.get("sid"), user.get("name"))

    face_stream = request.files.get('face_img').read()

    # 进行人脸检测，不存在人脸则不上传
    if not FaceTool(face_stream).is_face():
        return params_error(message='图像上没有人脸')

    # 这里先不更新人脸编码 TODO
    qiniu.upload_file(filename, face_stream)
    return success(data=qiniu.get_file(filename), message='图像上传成功')


@api.route('/face_detection', methods=['POST'])
def upload_tmp():
    filename = "tmp-{}.png".format(str(int(time.time())))
    img_stream = request.files.get('img').read()

    buf = np.asarray(bytearray(img_stream), dtype="uint8")
    img = cv2.imdecode(buf, cv2.IMREAD_COLOR)
    result = detector.detect_faces(img)

    print(result)

    bounding_box = result[0]['box']
    keypoints = result[0]['keypoints']


    cv2.rectangle(img,
                  (bounding_box[0], bounding_box[1]),
                  (bounding_box[0] + bounding_box[2], bounding_box[1] + bounding_box[3]),
                  (0, 155, 255),
                  2)
    cv2.circle(img, (keypoints['left_eye']), 2, (0, 255, 0), 2)
    cv2.circle(img, (keypoints['right_eye']), 2, (0, 255, 0), 2)
    cv2.circle(img, (keypoints['nose']), 2, (0, 255, 0), 2)
    cv2.circle(img, (keypoints['mouth_left']), 2, (0, 255, 0), 2)
    cv2.circle(img, (keypoints['mouth_right']), 2, (0, 255, 0), 2)

    cv2.imwrite(filename, img)
    with open(filename, 'rb') as f:
        qiniu.upload_file(filename, f.read())
    os.remove(filename)
    return filename
