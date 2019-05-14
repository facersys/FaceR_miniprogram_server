# -*- coding: utf-8 -*-

import cv2
import numpy as np
import requests
import face_recognition
from apps.Config import getConfig
from apps.Library import mongo


class FaceTool:
    def __init__(self, img):
        """
        :param img: 图片地址或数据流
        """
        self.__img = img

    def is_face(self):
        if type(self.__img) == str:
            stream = requests.get(self.__img).content
        else:
            stream = self.__img

        image = cv2.imdecode(np.frombuffer(stream, np.uint8), cv2.IMREAD_COLOR)
        return True if face_recognition.face_encodings(image) else False

    def encode(self):
        """编码"""
        if type(self.__img) == str:
            stream = requests.get(self.__img).content
        else:
            # stream = BytesIO(self.__img).read()
            stream = self.__img

        image = cv2.imdecode(np.frombuffer(stream, np.uint8), cv2.IMREAD_COLOR)
        face_codes = list(face_recognition.face_encodings(image))

        if len(face_codes) <= 0:
            return False
        return face_codes[0].tolist()

    def face_detection(self):
        if type(self.__img) == str:
            stream = requests.get(self.__img).content
        else:
            stream = self.__img
        image = cv2.imdecode(np.frombuffer(stream, np.uint8), cv2.IMREAD_COLOR)
        face_landmarks_ = face_recognition.face_landmarks(image)
        return face_landmarks_

    def get_face_arr(self):
        if type(self.__img) == str:
            stream = requests.get(self.__img).content
        else:
            stream = self.__img

        image = cv2.imdecode(np.frombuffer(stream, np.uint8), cv2.IMREAD_COLOR)
        return image

    def find_face(self):
        """找到人脸"""
        return_result = []
        if type(self.__img) == str:
            stream = requests.get(self.__img).content
        else:
            stream = self.__img

        image = cv2.imdecode(np.frombuffer(stream, np.uint8), cv2.IMREAD_COLOR)
        face_locations = face_recognition.face_locations(image)

        # 画一下人脸框
        [cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0)) for (top, right, bottom, left) in
         face_locations]

        if not face_locations:
            return []
        try:
            face_codes = face_recognition.face_encodings(image, face_locations)
            # 这里允许多人脸同时签到
            if face_codes:
                for face_code in face_codes:
                    result = self.find_face_owner(face_code)
                    if result.get('code') == 0:
                        # 只有数据库的学生才可以签到
                        return_result.append(result.get('data'))
                    else:
                        return_result.append({'sid': -1})
        except Exception as e:
            print(e)
            pass

        return return_result, image

    def find_face_owner(self, face_code):
        results = list(mongo.find(getConfig('mongodb', 'user_collection'), {}))
        know_face_codes = [result['face'] for result in results]
        face_compare_result = face_recognition.compare_faces(know_face_codes, face_code)
        # 这里可能会出现非常相似的人脸(双胞胎) 不考虑
        try:
            user_index = face_compare_result.index(True)
        except ValueError:
            return {'code': 404, 'data': None}
        user = results[user_index]
        return {'code': 0, 'data': user}

# if __name__ == '__main__':
#     ft = FaceTool("https://facer.yingjoy.cn/static/logo.png")
#     cv2.imshow('', ft.get_face_arr())
#     cv2.waitKey(0)
