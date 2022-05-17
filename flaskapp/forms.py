from flask_login import user_accessed
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField
from wtforms.validators import InputRequired
from flask_wtf.file import FileField

class RegisterForm(FlaskForm):
    username = StringField('Username')
    email = StringField('Email')
    password = StringField('Password')
    confirm_password = StringField('Confirm password')

class LoginForm(FlaskForm):
    user = StringField('Username or email')
    password = StringField('Password')

class CTFDLoginForm(FlaskForm):
    username = StringField('Username', [InputRequired()])
    password = StringField('Password', [InputRequired()])

class EntryForm(FlaskForm):
    title = StringField('Title', [InputRequired()])
    description = StringField('Description')
    category = StringField('Category')
    points = IntegerField('Points')
    file = FileField('Challenge Files')