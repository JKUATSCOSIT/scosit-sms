# -*- coding: utf-8 -*-

from flask import jsonify
from . import api


@api.route('/')
def index():
    response = jsonify(message="app is running")
    return response, 200
