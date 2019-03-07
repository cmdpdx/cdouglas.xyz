from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, HiddenField
from wtforms.validators import DataRequired, Length

class PostForm(FlaskForm):
    id_ = HiddenField('id')
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    body = TextAreaField('Post body', validators=[DataRequired()])
    tags = StringField('Tags')
    public = BooleanField('Make public')

