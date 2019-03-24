# -*- coding: utf-8 -*-

from apps import create_app
from flask import render_template

__author__ = "YingJoy"

app = create_app()


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=443, ssl_context=('cert/server.crt', 'cert/server.key'))
    app.run(host='0.0.0.0', port=5001)
