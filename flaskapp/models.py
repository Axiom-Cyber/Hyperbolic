from flaskapp import db, login_manager
from flask_login import UserMixin
from datetime import datetime


'''
from flaskapp import db
db.create_all()
'''

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    display_name = db.Column(db.String(30), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    image_file = db.Column(db.String(30), nullable=False, default='default.png')
    is_activated = db.Column(db.Boolean, default=False, nullable=False)
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    last_login = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())


    def __repr__(self):
        return '<User %r>' % self.username