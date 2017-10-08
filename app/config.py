# -*- coding:utf-8 -*-

"""Configures the application
"""

import os


class Config(object):
    """Base configuration class
    """
    DEBUG = False
    TESTING = False
    SECRET_KEY = "I\xf9\x9cF\x1e\x04\xe6\xfaF\x8f\xe6)-\xa432"
    CSRF_ENABLED = True
    REDIS_URL = "redis://:{password}@{host}:{port}/{db}".format(
        password=os.getenv("REDIS_PASSWORD", "password"),
        host=os.environ.get("REDIS_HOST", "localhost"),
        port=os.environ.get("REDIS_PORT", "6379"),
        db=os.environ.get("REDIS_DB", "scosit-sms")
    )

    CELERY_RESULT_BACKEND = "redis://:{password}@{host}:{port}".format(
        password=os.getenv("REDIS_PASSWORD", "password"),
        host=os.environ.get("REDIS_HOST", "localhost"),
        port=os.environ.get("REDIS_PORT", "6379")
    )

    CELERY_BROKER_URL = "redis://:{password}@{host}:{port}".format(
        password=os.getenv("REDIS_PASSWORD", "password"),
        host=os.environ.get("REDIS_HOST", "localhost"),
        port=os.environ.get("REDIS_PORT", "6379")
    )



class DevelopmentConfig(Config):
    """Development Mode configuration
    """
    DEBUG = True
    CSRF_ENABLED = False

class TestingConfig(Config):
    """Testing mode configuration
    """
    TESTING = True
    CSRF_ENABLED = False


class ProductionConfig(Config):
    """Production Mode configuration
    """
    pass

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
}     