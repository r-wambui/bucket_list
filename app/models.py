from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from passlib.apps import custom_app_context as pwd_context

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
db = SQLAlchemy(app)


class User(db.Model):
    ___tablename__ = "user"

    def __init__(self, username, password):
        self.username = username
        self.password = pwd_context.encrypt(password)

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30))
    password = db.Column(db.String)
    bucketlists = db.relationship(
        "Bucketlist", backref="user_model", lazy="dynamic")
    bucketitems = db.relationship(
        "BucketlistItem", backref="user_model", lazy="dynamic")

    def verify_password(self, password):
        return pwd_context.verify(password, self.password)

    def generate_auth_token(self, expiration=3600):
        Serialize = Serializer(app.config['SECRET_KEY'],
                               expires_in=expiration)
        return Serialize.dumps({"id": self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        return User.query.get(data['id'])


class Bucketlist(db.Model):
    __tablename__ = "bucketlist"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    date_created = db.Column(db.DateTime, default=datetime.now, nullable=False)
    date_modified = db.Column(
        db.DateTime, default=datetime.now,
        onupdate=datetime.now, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey("user.id"))
    bucketitems = db.relationship(
        "BucketlistItem", backref="bucketlist", lazy="dynamic")


class BucketlistItem(db.Model):
    ___tablename__ = "bucketlist_item"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    date_created = db.Column(db.DateTime, default=datetime.now, nullable=False)
    date_modified = db.Column(
        db.DateTime, default=datetime.now, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey("user.id"))
    bucketlist_id = db.Column(db.Integer, db.ForeignKey("bucketlist.id"))
    done = db.Column(db.Boolean, default=False)
