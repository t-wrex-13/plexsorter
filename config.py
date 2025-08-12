import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PLEX_BASEURL = os.environ.get('PLEX_BASEURL', 'http://192.168.4.1:13703')
    PLEX_TOKEN = os.environ.get('PLEX_TOKEN', 'token')
    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'password')
    
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    DEBUG = True