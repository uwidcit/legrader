from main import app
from models import db, Movie
import csv



db.create_all(app=app)

with open('movies.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=',')
    for row in reader:
        movie = Movie(
            title=row['title'],
            release_date=row['release_date'],
            poster_url=row['poster_url'],
            studio=row['studio'],
            gross=row['worldwide_gross'],
            rating=row['rating']
        )
        db.session.add(movie)
    db.session.commit()

print('database initialized!')