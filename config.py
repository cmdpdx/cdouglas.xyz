import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    # App specific configs
    BLOG_TITLE = 'Read the Documentation'
    BLOG_DESCRIPTION = 'A blog about learning new things.'

    # Flask configurations
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'this-issomelong#sentence'
    
    # SQLAlchemy (DB)
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or \
        'sqlite:///' + os.path.join(basedir, 'cdouglas.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Internationalization
    LANGUAGES = ['en', 'es']