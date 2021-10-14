from os.path import join, dirname, realpath

class Config:
    UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'static/img')
    SECRET_KEY = 'SUPER SECRET'
    SQLALCHEMY_DATABASE_URI = 'mariadb+mariadbconnector://admin:password@127.0.0.1:3306/FlowySI'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_SAMESITE='Lax'
    UPLOAD_FOLDER = UPLOAD_FOLDER