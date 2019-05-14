# -*- coding: utf-8 -*-

from flask import Blueprint

pages = Blueprint('pages', __name__)

from apps.Pages import cciip
