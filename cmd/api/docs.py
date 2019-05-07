from flask import render_template, g, request

from cmd.api import bp
from cmd.api.blog import get_url_base


@bp.before_app_request
def before_request():
    g.url_base = get_url_base(request)

@bp.route('/docs')
def index():
    return render_template('api/index.html')

@bp.route('/docs/blog')
def blog():
    return render_template('api/blog_api.html')