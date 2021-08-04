from flask import Blueprint

panel = Blueprint('panel', __name__, url_prefix='/panel')

from . import views