# -*- coding: utf-8 -*-

from flask import Blueprint

__author__ = "YingJoy"

api = Blueprint("api", __name__, url_prefix='/api')

from apps.api import user
from apps.api import tool
from apps.api import notice
from apps.api import login
