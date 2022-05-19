from flask import url_for, render_template, request, jsonify, make_response, redirect, abort, flash
from flaskapp import app, csrf, bcrypt, db, login_manager, s, mail
from flaskapp.forms import CTFDLoginForm, EntryForm, LoginForm, RegistrationForm
from flaskapp.models import User
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.utils import secure_filename
from itsdangerous.exc import SignatureExpired
from flask_mail import Message
from datetime import datetime

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.user.data).first()
        if not user:
            user = User.query.filter_by(email=form.user.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=True)
            user.last_login = datetime.utcnow()
            db.session.commit()
            return redirect(url_for('index'))
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, display_name=form.display_name.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        send_verify_email(form.email.data)

        return redirect(url_for('login'))
    return render_template('register.html', form=form)

def send_verify_email(email):
    token = s.dumps(email, salt='email-confirm')
    link = url_for('confirm_email', token=token)
    msg = Message(f'Confirm Email', sender='mailman.hyperbolic@gmail.com', recipients=[email])
    msg.body = f'<a href={link}>Click to confirm</a>'
    mail.send(msg)

@app.route('/confirm-email/<token>')
def confirm_email(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age=600)
        user = User.query.filter_by(email=email).first()
        user.is_activated = True
        db.session.commit()
    except SignatureExpired:
        return 'Token is expired'
    return 'Token works'

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    return 'ya'

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.errorhandler(404)
def not_found(error):
    return make_response(render_template('404.html'), 404)


@app.errorhandler(400)
def bad_request():
    return make_response(render_template('400.html'), 400)


@app.errorhandler(500)
def server_error():
    return make_response(render_template('500.html'), 500)