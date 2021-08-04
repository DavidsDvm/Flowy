from flask import Flask

from .config import Config
from .auth import auth
from .panel import panel
from .models import db

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    app.register_blueprint(auth)
    app.register_blueprint(panel)

    db.init_app(app)
    return app