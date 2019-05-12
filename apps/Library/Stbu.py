# -*- coding: utf-8 -*-

import re
import json
import time
import requests

from apps.Library import qiniu, log
from apps.Library.FaceTools import FaceTool
from apps.Library.ImageTools import img2txt


class Stbu:
    def __init__(self, username, password):
        self.__username = username
        self.__password = password
        self.__session = requests.session()

        self.__headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "http://jw.stbu.edu.cn",
            "Referer": "http://jw.stbu.edu.cn/service/login.html"
        }

    def get_info(self):
        """获取信息"""
        html = self.__session.get("http://jw.stbu.edu.cn/vatuu/StudentInfoAction?setAction=studentInfoQuery",
                                  headers=self.__headers).text

        sid = re.search(r'学号.*?&nbsp;(\d+)</td>', html, re.S).group(1).strip()
        name = re.search(r'学生姓名.*?&nbsp;(.*?)</td>.*?护照', html, re.S).group(1).strip()
        gender = re.search(r'性别.*&nbsp;(.*?)</td>.*?出', html, re.S).group(1).strip()
        id_num = re.search(r'>身份证号.*?&nbsp;(.*?)</td>.*?考', html, re.S).group(1).strip()
        grade = re.search(r'当前年级.*?&nbsp;(.*?)</td>.*?就读', html, re.S).group(1).strip()
        major = re.search(r'就读专业.*?&nbsp;(.*?)</td>.*?专业', html, re.S).group(1).strip()
        classname = re.search(r'专业班级.*?&nbsp;(.*?)</td>.*?国标', html, re.S).group(1).strip()
        college = re.search(r'专业学院.*?&nbsp;(.*?)</td>.*?当前', html, re.S).group(1).strip()
        phone = re.search(r'宿舍电话.*?&nbsp;(.*?)</td>.*?母亲', html, re.S).group(1).strip()
        email = re.search(r'电子邮件.*?&nbsp;(.*?)</td>.*?学生', html, re.S).group(1).strip()

        face, img_content = self.get_face()
        filename = "{}-{}-{}-face.png".format(str(int(time.time())), sid, name)
        if qiniu.upload_file(filename, img_content):
            return {
                "sid": sid,
                "name": name,
                "id_num": id_num,
                "gender": gender,
                "grade": grade,
                "major": major,
                "cname": classname,
                "college": college,
                "face": face,
                "face_url": filename,
                "email": email,
                "phone": phone
            }
        return False

    def get_face(self):
        img_content = self.__session.get("http://jw.stbu.edu.cn/vatuu/StudentPhotoView").content
        face = FaceTool(img_content)

        return face.encode(), img_content

    def sync(self):
        self.__session.get("http://jw.stbu.edu.cn/service/login.htm")

        while True:
            response = self.__session.get(
                "http://jw.stbu.edu.cn/vatuu/GetRandomNumberToJPEG?test=%s" % int(time.time() * 1000))

            ranstring = img2txt(response.content)
            data = {
                "username": self.__username,
                "password": self.__password,
                "url": "http://jw.stbu.edu.cn/vatuu/UserLoginAction",
                "returnUrl": "",
                "area": "",
                "ranstring": ranstring
            }

            response = self.__session.post("http://jw.stbu.edu.cn/vatuu/UserLoginAction", data=data,
                                           headers=self.__headers)
            response.encoding = "utf-8"
            if "登录成功" in response.text:
                data = {
                    "url": "http://jw.stbu.edu.cn/vatuu/UserLoadingAction",
                    "returnUrl": "",
                    "loginMsg": json.loads(response.text)["loginMsg"]
                }
                self.__session.post("http://jw.stbu.edu.cn/vatuu/UserLoadingAction", data=data)
                return self.get_info()

            if "验证码输入不正确" in response.text:
                log.logger.debug('自动登陆教务系统，验证码输入不正确')
            elif "密码输入不正确" in response.text:
                return 0
            else:
                return
