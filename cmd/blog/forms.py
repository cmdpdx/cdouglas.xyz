from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Length

class PostForm(FlaskForm):
    id_ = HiddenField('id')
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    body = TextAreaField('Post body', validators=[DataRequired()])
    public = BooleanField('Make public')
    #save = 
    #submit = SubmitField('Submit post')

