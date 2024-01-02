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
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String)
    rating = db.Column(db.Float, nullable=False)
    ranking = db.Column(db.Integer)
    review = db.Column(db.String, nullable=False)
    img_url = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"Title: {self.title}, Year: {self.year}"

with app.app_context():
    db.create_all()

# creating a wtform that updated the rating and review
class MovieForm(FlaskForm):
    rating = IntegerField('Rating', validators=[DataRequired()])
    review = StringField("Review", validators=[DataRequired()])
    submit = SubmitField("Submit")


@app.route("/")
def home():
    # Execute a SQL Select query on the Movie model and retrieve the result set as scalar values(Single value)
    movies_query = db.session.execute(db.select(Movie).order_by(Movie.id)).scalars()
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

if __name__ == '__main__':
    app.run(debug=True)
