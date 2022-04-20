from flask import Flask
from flask_wtf.csrf import CSRFProtect
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

csrf = CSRFProtect(app)

from flaskapp import routes