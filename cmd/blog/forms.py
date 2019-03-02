from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    body = TextAreaField('Post body', validators=[DataRequired()])
    public = BooleanField('Make public')
    submit = SubmitField('Submit post')

