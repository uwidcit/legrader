from main import app
from models import db, Movie
import csv



db.create_all(app=app)

with open('movies.csv', newline='') as csv_file:
  data = csv.DictReader(csv_file, delimiter=',')
  for movies in data:
    movie = Movie(
      title = movies['title'],
      release_date = movies['release_date'],
      poster_url = movies['poster_url'],
      studio = movies['studio'],
      gross = movies['worldwide_gross'],
      rating = movies['rating'] 
    )
    db.session.add(movie)
  db.session.commit()  

print('database initialized!')