from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import config

db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.jinja_env.policies['json.dumps_kwargs'] = {'sort_keys': False}  # https://stackoverflow.com/questions/67214142/why-does-jinja2-filter-tojson-sort-keys
    app.config['JSON_SORT_KEYS'] = False  # https://stackoverflow.com/questions/43263356/prevent-flask-jsonify-from-sorting-the-data
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    return app


from app import models
