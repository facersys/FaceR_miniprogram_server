# -*- coding: utf-8 -*-

import cv2
import numpy as np
import requests

img_bytes = requests.get('https://facer.yingjoy.cn/static/logo.png').content

image = cv2.imdecode(np.frombuffer(img_bytes, np.uint8), cv2.IMREAD_COLOR)

img_encode = cv2.imencode('.png', image)[1]
data = np.array(img_encode).tostring()
print(data)
# pil_image.show()
# cv2.imshow('', image)
# cv2.waitKey(0)
