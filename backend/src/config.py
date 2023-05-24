import logging
import os
from datetime import timedelta
from pathlib import Path
from dotenv import load_dotenv, find_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=1)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') \
                              or 'postgresql://postgres:1@localhost:5432/bas'
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL') or 'redis://127.0.0.1:6379/0'
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND') or 'redis://127.0.0.1:6379/0'
    CELERY_ACCEPT_CONTENT = ['pickle', 'application/json']
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


# TODO remove - this is the contents of .flaskenv
# FLASK_APP=app.py
# FLASK_DEBUG=1
# FLASK_RUN_HOST=0.0.0.0
# FLASK_RUN_PORT=80
# FLASK_CONFIG=development


def pwt_args():
    """
    :return playwright arguments to launch_persistent_context depending on development or production environment
    """
    load_dotenv(find_dotenv('.env.dev'))

    pwt_dev_args = {
        "args": [''],
        "headless": False,
        "slow_mo": 100,
        # removed user_agent header because cloudflare did not let it pass
        # "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
        "user_data_dir": ""
    }

    pwt_prod_update_args = {
        "headless": True,
        "slow_mo": 500,
    }

    logging.info(f"environment {os.getenv('ENVIRONMENT')}")
    pwt_arguments = pwt_dev_args
    if not os.getenv('ENVIRONMENT') == 'dev':
        pwt_arguments.update(pwt_prod_update_args)
    return pwt_arguments
