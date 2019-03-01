from flask import Blueprint

bp = Blueprint('main', __name__)

from cmd.main import routes