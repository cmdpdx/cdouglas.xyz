import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    # App specific configs
    APP_NAME = 'cdouglas.xyz'
    BLOG_TITLE = 'Read the Documentation'
    BLOG_DESCRIPTION = 'A blog about learning new things.'
    LOG_TO_STDOUT = False
    CONTACT_EMAIL = 'cdouglas.xyz@gmail.com'

    # Flask configurations
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'this-issomelong#sentence'
    
    # SQLAlchemy (DB)
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or \
        'sqlite:///' + os.path.join(basedir, 'cdouglas.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Internationalization
    LANGUAGES = ['en', 'es']

    # Email settings
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['cdouglas.xyz@gmail.com']