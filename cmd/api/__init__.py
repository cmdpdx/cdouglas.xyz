from flask import Blueprint

bp = Blueprint('api', __name__)

from cmd.api import blog, errors, tokens, docs