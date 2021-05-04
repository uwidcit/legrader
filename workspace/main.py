import json
from flask_cors import CORS
from flask import Flask, request, render_template, redirect, flash, url_for, jsonify
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
    return render_template('app.html', movie=None)

@app.route('/movies/<id>')
def show_movie(id):
    # get all movies, the movie specified by id & its comments and pass all to the template
    return render_template('app.html', movie=None)    

@app.route('/comments', methods=['POST'])
def create_comment_action():
    return redirect(request.referrer) # redirect to previous page

@app.route('/deleteComment/<id>', methods=['GET'])
def delete_comment_action(id):
    return redirect(request.referrer)

################ Question 3 #####################

@app.route('/app')
def client_app():
  return app.send_static_file('app.html')

@app.route('/api/movies', methods=['GET'])
def get_movies():
  return 'result'

@app.route('/api/movies/<id>', methods=['GET'])
def get_movie(id):
  return 'result'

@app.route('/api/comments', methods=["POST"])
def create_comment():
    return 'result'

#get comments by movie id
@app.route('/api/movies/<id>/comments', methods=["GET"])
def get_movie_comments(id): 
    return 'result'

# get comment by comment id
@app.route('/api/comments/<id>', methods=["DELETE"])
def delete_comment(id): 
    return 'result'



if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080, debug=True)
