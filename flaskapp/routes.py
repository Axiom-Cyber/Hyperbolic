import re
from typing import List
from flask import send_file, url_for, render_template, request, jsonify, make_response, redirect, abort, flash
from flaskapp import app, socketio, csrf, bcrypt, db, login_manager, s, mail
from flaskapp.forms import LoginForm, RegistrationForm, ForgotPassword, ChangePassword, FileUploadForm, AdminUploadForm
from flaskapp.models import User
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.utils import secure_filename
from itsdangerous.exc import SignatureExpired
from flask_mail import Message
import hyperbola
import os
import shutil
from datetime import datetime
from filetype import guess
import flask

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('dashboard'))

@app.route('/')
def about():
    return render_template('about.html', title='About')

@app.route('/login/', methods=['GET', 'POST'])
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
            return redirect(url_for('dashboard'))
    return render_template('login.html', form=form, title='Login')

@app.route('/register/', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
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

@app.route('/confirm-email/<token>/')
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

@app.route('/forgot-password/', methods=['GET', 'POST'])
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

@app.route('/reset-password/<token>/', methods=['GET', 'POST'])
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
            return redirect(url_for('dashboard'))
    except SignatureExpired:
        msg = 'Password reset link is expired. Try again.'
    except Exception:
        msg = 'There were some issues with resetting your password. Try again.'
    return render_template('reset-password.html', form=form, title='Reset Password', msg=msg)

@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('dashboard'))

@app.route('/dashboard/')
@app.route('/dashboard/', methods=['GET', 'POST'])
def dashboard():
    upload = FileUploadForm()
    admin = AdminUploadForm()
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
    names = hyperbola.Commander.compile_names()
    return render_template('dashboard.html', title='Dashboard', upload=upload, admin=admin, form=form, names=names, logged=current_user.is_authenticated)

@app.route('/demos/')
def demos():
    return render_template('demo.html', title='Demos')

@app.route('/demos/plaintext-search/')
def demos_plaintext_search():
    return render_template('demos/plaintext-search.html', title='Plaintext Search Demo')

@app.route('/demos/decompress/')
def demos_decompress():
    return render_template('demos/decompress.html', title='Decompress Demo')

@app.route('/demos/bitmap/')
def demos_bitmap():
    return render_template('demos/bitmap.html', title='Bitmap Image Rendering Demo')

@app.route('/demos/cookies/')
def demos_cookies():
    return render_template('demos/cookies.html', title='Cookies Demo')

@app.route('/demos/cookies/set/')
def demos_cookies_set():
    resp = make_response(render_template('demos/cookies.html', title='Cookies Demo'))
    resp.set_cookie('demo-cookie', 'flag{oh_cool_this_checks_cookies}')
    return resp

@app.route('/demos/cookies/delete/')
def demos_cookies_delete():
    resp = make_response(render_template('demos/cookies.html', title='Cookies Demo'))
    resp.set_cookie('demo-cookie', 'I am cookie', 0)
    return resp

@app.route('/demos/directories/')
def demos_directories():
    return render_template('demos/directories.html', title='Webpage Directory Traversal Demo')

@app.route("/download/folder/<path:path>")
def download_folder(path):
    shutil.make_archive(path, 'zip', path)
    return flask.send_file("../" + path+".zip", as_attachment=True)

@app.route("/download/file/<path:path>")
def download_file(path):
    return send_file("../" + path, as_attachment=True)

@app.route('/docs')
def docs():
    return render_template('docs.html', title='Documentation')

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
    def __call__(self, type, msg=''):
        self.socket.emit('send_output', (type, msg), to=self.id)

@socketio.on('disconnect')
def delete():
    if os.path.isdir('flaskapp/static/UploadedFiles/'+request.sid):
        shutil.rmtree('flaskapp/static/UploadedFiles/'+request.sid)

@socketio.event
def search_text(data, user_problems, disabled, flag):
    disabled = disabled if isinstance(disabled, list) else []
    for i in user_problems:
        for j in user_problems[i]:
            j.replace(r'[^|\n].*?import.*?[$|\n]','')
    hyperbola.Commander.run('text', data, Logger(request.sid, socketio), 'flaskapp/UploadedFiles', user_problems, disabled, flag)

@socketio.event
def search_file(data, user_problems, disabled, flag):
    disabled = disabled if isinstance(disabled, list) else []
    path = "flaskapp/static/UploadedFiles/"+request.sid+"/"
    if not os.path.isdir(path):
        os.mkdir(path)
    path += secure_filename(data["name"])
    with open(path, "wb") as file: 
        file.write(data["binary"])
    if (guess(path) and guess(path).extension in ['jpeg', 'gif', 'png', 'apng', 'svg', 'bmp']):
        socketio.emit("send_output", ('image', "/static/UploadedFiles/" + request.sid + "/" + secure_filename(data["name"])))
    for i in user_problems:
        for j in user_problems[i]:
            j.replace(r'[^|\n].*?import.*?[$|\n]','')
    hyperbola.Commander.run('filepath', path, Logger(request.sid, socketio), user_problems, disabled, flag)

@socketio.event
def upload_file(data, desc):
    if current_user.is_authenticated:
        ret = hyperbola.add_solver(data["binary"], secure_filename(data["name"]), desc)
        if ret:
            socketio.emit('uploaded')
