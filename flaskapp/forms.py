from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField
from wtforms.validators import InputRequired

class CTFDLoginForm(FlaskForm):
    username = StringField('Username', [InputRequired()])
    password = StringField('Password', [InputRequired()])
    submit = SubmitField('Submit')

class EntryForm(FlaskForm):
    title = StringField('Title', [InputRequired()])
    description = StringField('Description', [])
    category = StringField('Category', [])
    points = IntegerField('Points', [])
    submit = SubmitField('Submit')