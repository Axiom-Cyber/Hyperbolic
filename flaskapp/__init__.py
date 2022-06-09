from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
import os
import secrets
from itsdangerous import URLSafeTimedSerializer
from flask_cors import CORS
from flask_socketio import SocketIO

app = Flask(__name__)

# $Env:VARIABLE_NAME = 'Value'
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') # secrets.token_urlsafe(32)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQL_URI') # 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.getenv('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.getenv('EMAIL_PASSWORD')

csrf = CSRFProtect(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
mail = Mail(app)
s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
CORS(app, resources={r'/*': {'origins': '*'}})
socketio = SocketIO(app)

from flaskapp import routes