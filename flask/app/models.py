import sqlalchemy
from app import db


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    follower_date = db.Column(db.Date(), nullable=True)
    following_date = db.Column(db.Date(), default=True, nullable=True)

    def __init__(self, username, follower_date=sqlalchemy.sql.null(), following_date=sqlalchemy.sql.null()):
        self.username = username
        self.follower_date = follower_date
        self.following_date =following_date
