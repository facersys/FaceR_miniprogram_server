# -*- coding: utf-8 -*-

from apps import create_app
from apps.Library import log
from flask import render_template, request

__author__ = "YingJoy"

app = create_app()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/test')
def hello_world():
    """
    用于测试服务器是否正常工作.
    """
    ua = request.headers['User-Agent']
    log.logger.debug("请求测试服务器是否正常工作")
    return ua + 'Hello World!  FaceR\'s API Working'


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=443,
        ssl_context=(
            r'C:\Users\Ying Joy\Documents\Code\PyCharm\FaceR_miniprogram_server\cert\server.crt',
            r'C:\Users\Ying Joy\Documents\Code\PyCharm\FaceR_miniprogram_server\cert\server.key'
        )
    )
    # app.run(host='0.0.0.0', port=5001)
