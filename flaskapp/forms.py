from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from flask_wtf.file import FileField
from flaskapp.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(5, 30)])
    display_name = StringField('Display name', validators=[DataRequired(), Length(5, 30)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(5, 120)])
    password = PasswordField('Password', validators=[DataRequired(), Length(12, 120)])
    confirm_password = PasswordField('Confirm password', validators=[DataRequired(), Length(12, 120), EqualTo('password')])
    submit = SubmitField('Sign up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username is already taken')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email is already taken')

class LoginForm(FlaskForm):
    user = StringField('Username or email', validators=[DataRequired(), Length(5, 30)])
    password = PasswordField('Password', validators=[DataRequired(), Length(12, 120)])
    submit = SubmitField('Login')

class ForgotPassword(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(5, 120)])
    submit = SubmitField('Send password reset')

class ChangePassword(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), Length(12, 120)])
    confirm_password = PasswordField('Confirm password', validators=[DataRequired(), Length(12, 120), EqualTo('password')])
    submit = SubmitField('Change password')

class CTFDLoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class EntryForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = StringField('Description')
    category = StringField('Category')
    points = IntegerField('Points')
    file = FileField('Challenge files')