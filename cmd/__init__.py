from flask import Flask, current_app, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_babel import Babel
from flask_moment import Moment

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
    app.register_blueprint(blog_bp, url_prefix="/blog")

    from cmd.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from cmd.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    return app

@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(current_app.config['LANGUAGES'])

from cmd import models