from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import hashlib
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE']
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = hashlib.sha256(password.encode()).hexdigest() 

    def __repr__(self):
        return '<User %r>' % self.username

class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,nullable=False)
    tsurami = db.Column(db.Numeric, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    annotation = db.Column(db.String(140))

    def __init__(self, user_id, tsurami, timestamp):
        self.user_id = user_id
        self.tsurami = tsurami
        self.timestamp = timestamp

    def __repr__(self):
        return '<ID:{0} User:{1} Tsurami:{2}>'.format(self.id, self.user_id, self.tsurami)

class Connection(db.Model):
    user_id = db.Column(db.Integer,nullable=False, primary_key=True, autoincrement=False)
    target_id = db.Column(db.Integer,nullable=False, primary_key=True, autoincrement=False)

    def __init__(self, user_id, target_id):
        self.user_id = user_id
        self.target_id = target_id
