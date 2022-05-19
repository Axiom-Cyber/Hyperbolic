from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
import os
import secrets
from itsdangerous import URLSafeTimedSerializer

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQL_URI'] # 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.environ['EMAIL_USER']
app.config['MAIL_PASSWORD'] = os.environ['EMAIL_PASSWORD']

csrf = CSRFProtect(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
mail = Mail(app)
s = URLSafeTimedSerializer(app.config['SECRET_KEY'])

from flaskapp import routes