import json
from flask_cors import CORS
from flask_login import LoginManager, current_user, login_user, login_required
from flask import Flask, request, render_template, redirect, flash, url_for, jsonify
from flask_jwt import JWT, jwt_required, current_identity
from sqlalchemy.exc import IntegrityError
from datetime import timedelta 

from models import db, Comment, Movie #add application models

''' Begin boilerplate code '''


def create_app():
  app = Flask(__name__, static_url_path='')
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
  app.config['SECRET_KEY'] = "MYSECRET"
  CORS(app)
  db.init_app(app)
  return app

app = create_app()

app.app_context().push()

''' End Boilerplate Code '''

################# Question 2 ##################
@app.route('/')
def index():
    movies = Movie.query.all()
    return render_template('app.html', movie=None, movies=movies)

@app.route('/movies/<id>')
def show_movie(id):
    movies = Movie.query.all()
    movie = Movie.query.get(id)
    comments = Comment.query.filter_by(movie_id=id)
    return render_template('app.html', movie=movie, movies=movies, comments=comments)    

@app.route('/comments', methods=['POST'])
def create_comment_action():
    data = request.form
    comment = Comment(username=data['username'], text=data['text'], movie_id=data['movie_id'])
    db.session.add(comment)
    db.session.commit()
    return redirect('/movies/'+data['movie_id'])

@app.route('/deleteComment/<id>', methods=['GET'])
def delete_comment_action(id):
    comment = Comment.query.get(id)
    db.session.delete(comment)
    db.session.commit()
    return redirect(request.referrer)

################ Question 3 #####################

@app.route('/app')
def client_app():
  return app.send_static_file('app.html')

@app.route('/api/movies', methods=['GET'])
def get_movies():
  movies = Movie.query.all()
  movies = [ movie.toDict() for movie in movies ]
  return jsonify(movies)

@app.route('/api/movies/<id>', methods=['GET'])
def get_movie(id):
  movie = Movie.query.get(id)
  return jsonify(movie.toDict())

@app.route('/api/comments', methods=["POST"])
def create_comment():
    data = request.json
    comment = Comment(username=data['username'], text=data['text'], movie_id=data['movie_id'])
    db.session.add(comment)
    db.session.commit()
    return jsonify({"message":"created"}), 201

@app.route('/api/movies/<id>/comments', methods=["GET"])
def get_movie_comments(id): 
    comments = Comment.query.filter_by(movie_id=id)
    comments = [ comment.toDict() for comment in comments ]
    return jsonify(comments)

@app.route('/api/comments/<id>', methods=["DELETE"])
def delete_comment(id): 
    comment = Comment.query.get(id)
    db.session.delete(comment)
    db.session.commit()
    return jsonify({"message":"deleted"}), 200



if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080, debug=True)