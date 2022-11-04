from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
import requests

#Form Packages
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

# Databse Configurations
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///movies.db'
db = SQLAlchemy(app)

#API DETAILS
MOVIE_DB_API_KEY = '9b8b84460e164a6db815fdbc4e26def1'
MOVIE_DB_SEARCH_URL = "https://api.themoviedb.org/3/search/movie"
MOVIE_DB_INFO_URL = "https://api.themoviedb.org/3/movie"
MOVIE_DB_IMAGE_URL = "https://image.tmdb.org/t/p/w500"

#Creating Models
class Movies(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(250), nullable=False, unique = True)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(500), nullable=True)
    rating = db.Column(db.Float, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    review = db.Column(db.String(250), nullable=True)
    img_url = db.Column(db.String(250), nullable=False)

with app.app_context():
    db.create_all() #It will create the movie table in the database


#Making Form
class FindMovieForm(FlaskForm):
    title = StringField("Movie Name", validators=[DataRequired()])
    submit = SubmitField("Add Movie")


#Routes and Views
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add', methods = ['POST', 'GET'])
def add_movies():
    form = FindMovieForm()
    if form.validate_on_submit():
        movie_title = form.title.data
        response = requests.get(MOVIE_DB_SEARCH_URL, params={'api_key' : MOVIE_DB_API_KEY, 'query': movie_title})
        data = response.json()["results"]
        print(data)
    return render_template('add.html', form = form)


if __name__ == '__main__':
    app.run(debug=True)