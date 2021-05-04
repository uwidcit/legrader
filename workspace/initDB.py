from main import app
from models import db, Movie, Comment
import csv

db.create_all(app=app)



print('database initialized!')
