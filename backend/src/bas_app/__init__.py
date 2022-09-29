import os

from flask import Flask
from flask_celeryext import FlaskCeleryExt
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import config

from .celery_utils import make_celery


db = SQLAlchemy()
migrate = Migrate()
ext_celery = FlaskCeleryExt(create_celery_app=make_celery)


def create_app(config_name):
    app = Flask(__name__)
    app.jinja_env.policies['json.dumps_kwargs'] = {
        'sort_keys': False}  # https://stackoverflow.com/questions/67214142/why-does-jinja2-filter-tojson-sort-keys
    app.config[
        'JSON_SORT_KEYS'] = False  # https://stackoverflow.com/questions/43263356/prevent-flask-jsonify-from-sorting-the-data
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    migrate.init_app(app, db, directory='migrations', render_as_batch=True)
    ext_celery.init_app(app)

    from .main import main as main_blueprint
    from .api.user import user as user_blueprint
    from .api.job import job as job_blueprint
    from .api.search import search as search_blueprint
    from .api.card import card as card_blueprint
    from .api.filter_visibility import filter_visibility as filter_visibility_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(job_blueprint)
    app.register_blueprint(search_blueprint)
    app.register_blueprint(card_blueprint)
    app.register_blueprint(filter_visibility_blueprint)

    return app


from . import models
