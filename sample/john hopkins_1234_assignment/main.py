from flask_cors import CORS
from flask import Flask, request, render_template, redirect, flash, url_for, jsonify
from sqlalchemy.exc import IntegrityError
from datetime import timedelta 

from models import db, Laptop #add application models

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

##### Question 2 Laptop Filter Function #####

def laptop_filter(laptops, brand='Any', display_size='Any', graphics_brand='Any', processor_brand='Any', price_range=13000):

  if price_range:
    laptops = list(filter(lambda laptop: int(laptop.price) < int(price_range), laptops))

  #add filters for brand, graphics, processor and display

  return laptops

############### Question 3 Routes ##########

@app.route('/')
def index():
  # get brand, display_size etc from query params
  # laptops = laptop_filter(laptops, brand, display_size, graphics_brand, processor_brand, price_range)
  return render_template('app.html')

@app.route('/deleteLaptop/<id>', methods=['GET'])
def delete_action(id):
  return 'delete action'

@app.route('/insertLaptop', methods=['POST'])
def insert_action():
  return 'insert action'

############### Question 4 Routes ###########

@app.route('/app')
def client_app():
  return app.send_static_file('app.html')

@app.route('/api/laptops', methods=['GET'])
def get_laptops():
  # get brand, display_size etc from query params
  # laptops = laptop_filter(laptops, brand, display_size, graphics_brand, processor_brand, price_range)
  return 'read data'

@app.route('/api/laptops', methods=['POST'])
def create_laptop():
  return 'create data'

@app.route('/api/delete/<id>', methods=['DELETE'])
def delete_laptops(id):
  return 'delete data'

#############################################


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080, debug=True)
