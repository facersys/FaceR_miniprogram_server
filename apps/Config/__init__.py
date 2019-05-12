# -*- coding: utf-8 -*-

try:
    import configparser
except:
    from six.moves import configparser

import os


def getConfig(section, key):
    config = configparser.ConfigParser()
    path = os.path.split(os.path.realpath(__file__))[0] + '/setting.ini'
    config.read(path)
    return config.get(section, key)


if __name__ == '__main__':
    print(getConfig('logger', 'format_str'))
