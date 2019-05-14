# -*- coding: utf-8 -*-

from flask import Blueprint

api = Blueprint("api", __name__, url_prefix='/api')

from apps.Interface import Login
from apps.Interface import Notice
from apps.Interface import User
from apps.Interface import FaceRecognition
from apps.Interface.User import Stbu
