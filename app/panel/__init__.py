from flask import Blueprint
from flask.helpers import url_for
from flask_login.utils import login_required
from werkzeug.utils import redirect

panel = Blueprint('panel', __name__, url_prefix='/panel')

@panel.before_request
@login_required
def before_request():
    pass

from . import views