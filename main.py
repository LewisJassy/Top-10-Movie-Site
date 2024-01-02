from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
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



@app.route("/")
def home():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)
