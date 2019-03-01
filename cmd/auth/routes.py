from flask import current_app, redirect, url_for, flash, request, render_template
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user

from cmd import db
from cmd.models import User
from cmd.auth import bp
from cmd.auth.forms import LoginForm

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Administrator login."""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        # failed password auth or username doesn't exist (don't differentiate)
        if user is None or not user.check_password(form.password.data):
            flash('Incorrect username or password.')
            return redirect(url_for('auth.login'))

        # Success
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)

    return render_template('auth/login.html', title='Login', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))