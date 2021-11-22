from os.path import join, dirname, realpath
from decouple import config as config_decouple
import os

class Config:
    UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'static/img')
    SECRET_KEY = 'SUPER SECRET'
    SQLALCHEMY_DATABASE_URI = 'mariadb+mariadbconnector://root:''@127.0.0.1:3306/FlowySI'
    if config_decouple('PRODUCTION', default=False):
        SQLALCHEMY_DATABASE_URI = (os.environ.get('DB_URL'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_SAMESITE='Lax'
    UPLOAD_FOLDER = UPLOAD_FOLDER