from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
import datetime


class Laptop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
