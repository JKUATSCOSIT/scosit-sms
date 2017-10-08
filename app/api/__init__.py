from flask import Blueprint

api = Blueprint(name='api')

from . import views, errors