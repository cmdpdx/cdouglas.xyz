from flask import Blueprint

bp = Blueprint('auth', __name__)

from cmd.auth import routes