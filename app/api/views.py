# -*- coding: utf-8 -*-

from flask import jsonify
from . import api


@api.route('/')
def index():
    response = jsonify(body="App is working!")
    return response, 200
