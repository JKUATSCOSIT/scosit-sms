# -*- coding:utf-8 -*-

"""Configures the application
"""

import os


class Config(object):
    """Base configuration class
    """
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
    Debug = True


class TestingConfig(Config):
    """Testing mode configuration
    """
    Testing = True


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