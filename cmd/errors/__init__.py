from flask import Blueprint

bp = Blueprint('errors', __name__)

from cmd.errors import handlers