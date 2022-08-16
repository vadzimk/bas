import os
from datetime import timedelta
from pathlib import Path

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=1)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(Path(basedir).parent, 'app.sqlite')
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL') or 'redis://127.0.0.1:6379/0'
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND') or 'redis://127.0.0.1:6379/0'
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # send a signal to application when a change is about to be made in the db

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI


class TestingConfig(Config):
    TESTING = True
    # SQLALCHEMY_DATABASE_URI


class ProductionConfig(Config):
    pass
    # SQLALCHEMY_DATABASE_URI


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
