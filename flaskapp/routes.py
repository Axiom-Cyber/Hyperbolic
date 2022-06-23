import re
from flask import url_for, render_template, request, jsonify, make_response, redirect, abort, flash
from flaskapp import app, socketio, csrf, bcrypt, db, login_manager, s, mail
from flaskapp.forms import CTFDLoginForm, EntryForm, LoginForm, RegistrationForm, ForgotPassword, ChangePassword, FileUploadForm
from flaskapp.models import User
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.utils import secure_filename
from itsdangerous.exc import SignatureExpired
from flask_mail import Message
import hyperbola
from datetime import datetime

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('login'))

@app.route('/')
def about():
    return redirect(url_for('dashboard'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():

        # Determine if username or email from database
        user = User.query.filter_by(username=form.user.data).first()
        if not user:
            user = User.query.filter_by(email=form.user.data).first()
        
        # Authenticate and execute login
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=True)
            user.last_login = datetime.utcnow()
            db.session.commit()
            return redirect(url_for('index'))
    return render_template('login.html', form=form, title='Login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()

    # Generate hash and save user info
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, display_name=form.display_name.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        send_verify_email(form.email.data)
        return redirect(url_for('dashboard'))
    return render_template('register.html', form=form, title='Register')

def send_verify_email(email):
    token = s.dumps(email, salt='email-confirm')
    link = url_for('confirm_email', token=token)
    msg = Message(f'Confirm Email', sender='Hyperbola', recipients=[email])
    msg.body = f'<a href={link}>Click to confirm</a>'
    mail.send(msg)

@app.route('/confirm-email/<token>')
def confirm_email(token):
    msg = 'There were some problems verifying your email. Try again.'
    try:
        email = s.loads(token, salt='email-confirm', max_age=600)
        user = User.query.filter_by(email=email).first()
        user.is_activated = True
        db.session.commit()
        msg = 'Your email is confirmed! You may exit out of this page.'
    except SignatureExpired:
        msg = 'Email verification link is expired. Try again.'
    except Exception:
        pass
    return render_template('confirm-email.html', title='Confirm Email', msg=msg)

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ForgotPassword()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = s.dumps(form.email.data, salt='reset-password')
            link = url_for('reset_password', token=token)
            msg = Message(f'Confirm Email', sender='Hyperbola', recipients=[form.email.data])
            msg.body = f'<a href={link}>Click to reset password</a>'
            mail.send(msg)
            return redirect(url_for('dashboard'))
    return render_template('forgot-password.html', form=form, title='Forgot Password')

@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    msg = None
    form = ChangePassword()
    try:
        email = s.loads(token, salt='reset-password', max_age=600)
        user = User.query.filter_by(email=email).first()
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user.password = hashed_password
            db.session.commit()
            return redirect(url_for('login'))
    except SignatureExpired:
        msg = 'Password reset link is expired. Try again.'
    except Exception:
        msg = 'There were some issues with resetting your password. Try again.'
    return render_template('reset-password.html', form=form, title='Reset Password', msg=msg)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard/')
def dashboard():
    form = CTFDLoginForm()
    upload = FileUploadForm()
    return render_template('dashboard.html', title='Dashboard', form=form, upload=upload)

@app.errorhandler(404)
def not_found(error):
    return make_response(render_template('404.html', title='404'), 404)


@app.errorhandler(400)
def bad_request():
    return make_response(render_template('400.html', title='400'), 400)


@app.errorhandler(500)
def server_error():
    return make_response(render_template('500.html', title='500'), 500)


## Sockets
class Logger:
    def __init__(self, id, socket):
        self.id = id
        self.socket = socket
    async def __call__(self, type, msg=''):
        self.socket.emit('send_output', (type, msg), to=self.id)
@socketio.event
def start_search(type, data):
    hyperbola.Commander.run(type, data, Logger(request.sid, socketio))

@socketio.event
def upload(data):
    file = open("flaskapp/UploadedFiles/" + secure_filename(data["name"]), "wb")
    file.write(data["binary"])
    file.close()