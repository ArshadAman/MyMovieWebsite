from flask import Flask, render_template, request
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
MOVIE_DB_API_KEY = ''
SEARCH_ENDPOINT = "https://api.themoviedb.org/3/search/movie"
MOVIE_INFO_ENDPOINT = "https://api.themoviedb.org/3/movie"
MOVIE_IMAGE_URL = "https://image.tmdb.org/t/p/w500"

#Creating Models
class Movies(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(250), nullable=False, unique = True)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(500), nullable=True)
    img_url = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    review = db.Column(db.String(250), nullable=True)

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
        response = requests.get(SEARCH_ENDPOINT, params={'api_key' : MOVIE_DB_API_KEY, 'query': movie_title})
        data = response.json()["results"]
        print(type(data))
        return render_template('select.html', movies = data)
    return render_template('add.html', form = form)

@app.route('/find')
def find_movie():
    movie_id = request.args.get("id")
    if movie_id:
        complete_endpoint = f"{MOVIE_INFO_ENDPOINT}/{movie_id}"
        response = requests.get(complete_endpoint, params={"api_key": MOVIE_DB_API_KEY})
        data = response.json()
        new_movie = Movies(
            title = data["title"],
            year = data["release_date"].split("-")[0],
            img_url = f"{MOVIE_IMAGE_URL}{data['poster_path']}",
            description = data["overview"],
        )
        db.session.add(new_movie)
        db.session.commit()
        return "Successfully Added"
    return "Some Error Occured"


if __name__ == '__main__':
    app.run(debug=True)
