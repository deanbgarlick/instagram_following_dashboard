from app import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    follower_date = db.Column(db.Date(), default=True, nullable=True)
    following_date = db.Column(db.Date(), default=True, nullable=True)

    def __init__(self, username):
        self.username = username