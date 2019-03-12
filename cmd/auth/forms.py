from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,  BooleanField, SubmitField
from wtforms.validators import DataRequired

from cmd.models import User


class LoginForm(FlaskForm):
    username = StringField('User', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember')
    submit = SubmitField('Log in')