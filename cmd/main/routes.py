from flask import render_template, url_for, flash, redirect, request, g, current_app

from cmd import db
from cmd.main import bp

@bp.before_app_request
def before_request():
    g.blog_title = current_app.config['BLOG_TITLE']
    g.contact_email = current_app.config['CONTACT_EMAIL']
    
@bp.route('/')
@bp.route('/index')
def index():
    return render_template('index.html')