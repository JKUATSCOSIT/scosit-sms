# -*- coding:utf-8 -*-

from flask import Flask
from flask_redis import FlaskRedis
from celery import Celery
from raven.contrib.flask import Sentry

from app.config import config, Config

celery = Celery(__name__,
                backend=Config.CELERY_RESULT_BACKEND,
                broker=Config.CELERY_BROKER_URL)

redis = FlaskRedis()

# sentry = Sentry(
#     dsn="https://a88a0c9e894a45bc8a6c3ad872d22c2e:"
#         "f5dcef4d47544b62a68b0d0501235366@sentry.io/227387")


def create_app(config_name):
    """Application factory to create the application
    :param: config_name - configuration name e.g Development
    :return: app
    :rtype: Flask application instance
    """

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    celery.conf.update(app.config)

    # sentry.init_app(app, logging=True)

    redis.init_app(app)

    # register blueprints
    from app.api import api as api_v1_blueprint

    app.register_blueprint(api_v1_blueprint, url_prefix="/api/version/1")

    return app