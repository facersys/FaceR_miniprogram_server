# -*- coding: utf-8 -*-

import time
from flask import render_template, request, flash
from apps.api import api
from apps.libs.face import FaceTool
from apps.models.user import UserModel


@api.route('/cciip', methods=['GET', 'POST'])
def cciip():
    if request.method == 'GET':
        return render_template('cciip.html')
    else:
        form = request.form
        files = request.files
        name = form.get('name')
        sid = form.get('sid')

        photo = files.get('photo').read()
        face = FaceTool(photo)

        try:
            face_code = face.encode()
            user = UserModel(name=name, sid=sid, face=face_code, source='cciip demo',
                             openid=str(int(time.time() * 1000)), unionid=str(int(time.time() * 1000)))
            if user.save():
                flash('success', 'success')
                return render_template('cciip.html')
            else:
                flash('sid exists', 'danger')
                return render_template('cciip.html')
        except IndexError:
            flash('no face in this photo', 'danger')
            return render_template('cciip.html')
