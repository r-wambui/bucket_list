from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../db.db'
app.config.from_object('config.DevelopmentConfig')
db = SQLAlchemy(app)

class UserModel(db.Model):
    ___tablename__ = "usermodel"

    def __init__(self,username,password):
        self.username = username
        self.password = password

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30))
    password = db.Column(db.String)
    # bucketlists = db.relationship(
    #     "Bucketlist", backref="created_by", lazy="dynamic")
    # bucketitems = db.relationship(
    #     "BucketlistItem", backref="created_by", lazy="dynamic")


class Bucketlist(db.Model):
    ___tablename__ = "bucketlist"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    date_created = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime)
    # created_by = db.Column(db.Integer, db.ForeignKey("usermodel.id"))
    # bucketitems = db.relationship(
    #     "BucketlistItem", backref="bucketlist", lazy="dynamic")


class BucketlistItem(db.Model):
    ___tablename__ = "bucketlist_item"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    date_created = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime)
    # created_by = db.Column(db.Integer, db.ForeignKey("usermodel.id"))
    # bucketlist_id = db.Column(db.Integer, db.ForeignKey("bucketlist.id"))
    done = db.Column(db.Boolean, default= False)
