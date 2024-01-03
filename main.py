from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired
import requests


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Movies.db"

db.init_app(app)

class Movie(db.Model):
    """Represents a movie in the database."""

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String)
    rating = db.Column(db.Float, nullable=False)
    ranking = db.Column(db.Integer)
    review = db.Column(db.String, nullable=False)
    img_url = db.Column(db.String, nullable=False)

    def __repr__(self):
        """Returns a string representation of the movie."""
        return f"Title: {self.title}, Year: {self.year}"

with app.app_context():
    db.create_all()

# creating a wtform that updated the rating and review
class MovieForm(FlaskForm):
    """Form for editing a movie's rating and review."""

    rating = IntegerField('Rating', validators=[DataRequired()])
    review = StringField("Review", validators=[DataRequired()])
    submit = SubmitField("Submit")

class MovieAddForm(FlaskForm):
    """Form for adding a new movie."""

    title = StringField('Title', validators=[DataRequired()])
    year = IntegerField('Year', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    rating = IntegerField('Rating', validators=[DataRequired()])
    ranking = IntegerField('Ranking', validators=[DataRequired()])
    review = StringField('Review', validators=[DataRequired()])
    img_url = StringField('Image URL', validators=[DataRequired()])
    submit = SubmitField('Add Movie')


def add_movie(title, year, description, rating, ranking, review, img_url):
    """Adds a new movie to the database."""

    movie = Movie(
        title=title,
        year=year,
        description=description,
        rating=rating,
        ranking=ranking,
        review=review,
        img_url=img_url
    )

    db.session.add(movie)
    db.session.commit()


@app.route("/")
def home():
    """Displays the home page with a list of movies."""
    
    # Execute a SQL Select query on the Movie model and retrieve the result set as scalar values(Single value)
    movies_query = db.session.execute(db.select(Movie).order_by(Movie.rating)).scalars().all()
    # This loop assigns rankings to movies based on their position in the sorted list, and the ranking are stored in the db
    # This type of ranking is often used when displaying a sorted list where the top item has the highest rank, the second item has the second-highest rank, and so on
    for i in range(len(movies_query)):
        movies_query[i].ranking = len(movies_query) - i
    db.session.commit()
    return render_template("index.html", movies=movies_query)


@app.route('/edit', methods=['GET', 'POST'])
def rate_movie():
    form = MovieForm()
    # get the value of the id param from the query string
    movie_id = request.args.get('id', None)
    movie = db.get_or_404(Movie, movie_id) if movie_id is not None else None
    if movie is not None:
        if form.validate_on_submit():
            movie.rating = float(form.rating.data)
            movie.review = form.review.data
            db.session.commit()
            return redirect(url_for("home"))
        return render_template("edit.html", form=form, movie=movie)
    else:
        # Handle the case where movie_id is not found
        return render_template("error.html", error_message="Movie not found")
    
@app.route("/delete/<int:movie_id>", methods=["GET", "POST"])
def delete(movie_id):
    delete_movie = Movie.query.get_or_404(movie_id)
    db.session.delete(delete_movie)
    db.session.commit()
    return redirect(url_for("home"))
    
@app.route('/add', methods=['GET', 'POST'])
def add_movie_route():
    form = MovieAddForm()

    if form.validate_on_submit():
        add_movie(
            title=form.title.data,
            year=form.year.data,
            description=form.description.data,
            rating=form.rating.data,
            ranking=form.ranking.data,
            review=form.review.data,
            img_url=form.img_url.data
        )
        return redirect(url_for("home"))

    return render_template("add.html", form=form)

if __name__ == '__main__':
    app.run(debug=True)
