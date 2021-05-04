from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
import datetime


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)





class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)