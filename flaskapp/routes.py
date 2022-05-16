from flaskapp import app, csrf
from flaskapp.forms import CTFDLoginForm, EntryForm
from flask import url_for, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os

values = {}

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def home(path):
    return render_template('home.html', **values)

@app.route("/heartbeat")
def heartbeat():
    return jsonify({"status": "healthy"})

@app.route("/hello", methods=["POST"])
@csrf.exempt
def hello():
    global values
    values['message'] = 'hello'
    return 'hello'

@app.route("/goodbye", methods=["POST"])
@csrf.exempt
def goodbye():
    global values
    values['goodbye'] = 'goodbye'
    return 'goodbye'