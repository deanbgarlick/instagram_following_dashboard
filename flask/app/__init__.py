from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object("app.config.Config")

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    day_followed = db.Column(db.Date(), default=True, nullable=True)
    day_following = db.Column(db.Date(), default=True, nullable=True)

    def __init__(self, username):
        self.username = username


from app import views
from app import scraper