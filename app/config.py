class Config:
    SECRET_KEY = 'SUPER SECRET'
    SQLALCHEMY_DATABASE_URI = 'mariadb+mariadbconnector://root:''@127.0.0.1:3306/FlowySI'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_SAMESITE='Lax'