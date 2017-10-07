"""Configures the application
"""
class Config(object):
    """Base configuration class
    """
    pass 

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