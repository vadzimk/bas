from flask import Blueprint

filter_visibility = Blueprint('filter_visibility', __name__)

from . import routes