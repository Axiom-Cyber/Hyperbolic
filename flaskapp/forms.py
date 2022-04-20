from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField
from wtforms.validators import InputRequired
from flask_wtf.file import FileField

class CTFDLoginForm(FlaskForm):
    username = StringField('Username', [InputRequired()])
    password = StringField('Password', [InputRequired()])

class EntryForm(FlaskForm):
    title = StringField('Title', [InputRequired()])
    description = StringField('Description')
    category = StringField('Category')
    points = IntegerField('Points')
    file = FileField('Challenge Files')