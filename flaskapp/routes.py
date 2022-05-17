from flask import url_for, render_template, request, jsonify, make_response, redirect, abort, flash
from flaskapp import app, csrf
from flaskapp.forms import CTFDLoginForm, EntryForm, LoginForm, RegisterForm
from flaskapp.models import User
from flask_login import login_user, logout_user, login_required
from werkzeug.utils import secure_filename

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        login_user(user)
        flash('Logged in successfully.')
        next = request.args.get('next')
        if not is_safe_url(next):
            return abort(400)

        return redirect(next or url_for('index'))
    return render_template('login.html', form=form)

@app.route('/register')
def register():
    return render_template('register.html')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.errorhandler(404)
def not_found():
    return make_response(render_template('404.html'), 404)


@app.errorhandler(400)
def bad_request():
    return make_response(render_template('400.html'), 400)


@app.errorhandler(500)
def server_error():
    return make_response(render_template('500.html'), 500)