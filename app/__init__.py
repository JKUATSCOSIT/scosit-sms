# -*- coding:utf-8 -*-

from flask import Flask
from flask_redis import FlaskRedis
from mockredis import MockRedis
from celery import Celery

from app.config import config, Config
from app.api import api

celery = Celery(__name__,
                backend=Config.CELERY_RESULT_BACKEND,
                broker=Config.CELERY_BROKER_URL)


def create_app(config_name):
    """Application factory to create the application
    :param: config_name - configuration name e.g Development
    :return: app
    :rtype: Flask application instance
    """
    app = Flask(__name__)
    app_config = config.get(config_name)
    app.config.from_object(app_config)

    celery.conf.update(app.config)

    if app.testing:
        # Use mock redis to make unit testing simpler
        redis = FlaskRedis.from_custom_provider(MockRedis)
    else:
        redis = FlaskRedis()

    redis.init_app(app)

    # register blueprints
    app.register_blueprint(api, url_prefix="/api/version/1")

    return app