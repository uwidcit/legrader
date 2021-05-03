from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
import datetime


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)

    def toDict(self):
        return{
            'id': self.id,
            'text': self.text,
            'username': self.username,
            'movie_id':self.movie_id
        }


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    release_date = db.Column(db.String(100), nullable=False)
    poster_url = db.Column(db.String(100), nullable=False)
    studio = db.Column(db.String(100), nullable=False)
    gross = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.String(5), nullable=False)
    comments = db.relationship('Comment', backref='movie', lazy=True)

    def toDict(self):
        return {
            "id":self.id,
            "title": self.title,
            "release_date": self.release_date,
            "studio": self.studio,
            "gross": self.gross,
            "poster_url" : self.poster_url
        }