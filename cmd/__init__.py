from flask import Flask, current_app, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_babel import Babel
from flask_moment import Moment

import os
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler

from config import Config

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
bootstrap = Bootstrap()
babel = Babel()
moment = Moment()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    bootstrap.init_app(app)
    babel.init_app(app)
    moment.init_app(app)

    from cmd.main import bp as main_bp
    app.register_blueprint(main_bp)

    from cmd.blog import bp as blog_bp
    app.register_blueprint(blog_bp, url_prefix='/blog')

    from cmd.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    from cmd.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from cmd.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    # Error logging/emailing 
    #if False:   # skip for now, turn back on before production
    if not app.debug and not app.testing:
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'], 
                        app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr=f"no-reply@{app.config['MAIL_SERVER']}",
                toaddrs=app.config['ADMINS'],
                subject=f"[{app.config['APP_NAME']}] Site failure",
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

        if app.config['LOG_TO_STDOUT']:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            app.logger.addHandler(stream_handler)
        else:
            if not os.path.exists('logs'):
                os.mkdir('logs')
            file_handler = RotatingFileHandler(
                f"logs/{app.config['APP_NAME']}.log", 
                maxBytes=10240,
                backupCount=10)
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s '
                '[in %(pathname)s:%(lineno)d]'))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info(app.config['APP_NAME'] + ' startup.')

    return app


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(current_app.config['LANGUAGES'])


from cmd import models