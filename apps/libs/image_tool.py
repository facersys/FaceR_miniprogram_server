# -*- coding: utf-8 -*-

from apps.libs import aipOcr


def img2txt(stream):
    """图片转文字"""
    result = aipOcr.basicAccurate(stream).get("words_result")
    return result[0].get('words') if result else ""
