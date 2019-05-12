# -*- coding: utf-8 -*-

import cv2
import numpy as np

from apps.libs import aipOcr


def img2txt(stream):
    """图片转文字"""
    result = aipOcr.basicAccurate(stream).get("words_result")
    return result[0].get('words') if result else ""


def get_polylines_data(arr):
    return [np.array([list(item) for item in arr], np.int32)]


def draw_face(image, face_landmarks_list):
    """画人脸"""
    for face_landmarks in face_landmarks_list:
        # 眉毛
        cv2.polylines(image, get_polylines_data(face_landmarks['left_eyebrow']), False, (0, 255, 0), 5)
        cv2.polylines(image, get_polylines_data(face_landmarks['right_eyebrow']), False, (0, 125, 0), 5)

        # 嘴唇
        cv2.polylines(image, get_polylines_data(face_landmarks['top_lip']), False, (255, 0, 255), 3)
        cv2.polylines(image, get_polylines_data(face_landmarks['bottom_lip']), False, (125, 0, 125), 3)

        # 眼睛
        cv2.polylines(image, get_polylines_data(face_landmarks['left_eye']), True, (0, 0, 255), 3)
        cv2.polylines(image, get_polylines_data(face_landmarks['right_eye']), True, (0, 0, 125), 3)

        # 下巴
        cv2.polylines(image, get_polylines_data(face_landmarks['chin']), False, (255, 255, 255), 3)

        # 鼻子
        cv2.polylines(image, get_polylines_data(face_landmarks['nose_bridge']), False, (255, 255, 0), 3)
        cv2.polylines(image, get_polylines_data(face_landmarks['nose_tip']), False, (125, 125, 0), 3)

    return image
