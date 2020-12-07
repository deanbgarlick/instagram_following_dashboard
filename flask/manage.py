import datetime
import json
from flask.cli import FlaskGroup

from app import app, db
from app.models import User
from app.views import get_db_engine


def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


def update_data():

    with open('./network.json', 'r') as f:
        network = json.load(f)

    following_accounts = set(network['following'])
    follower_accounts = set(network['followers'])

    following_and_follower = following_accounts & follower_accounts
    following_only = following_accounts.difference(follower_accounts)
    follower_only = follower_accounts.difference(following_accounts)

    for account in following_and_follower:
        u = User(username=account, follower_date=datetime.date.today(), following_date=datetime.date.today())
        db.session.add(u)
        db.session.commit()

    for account in following_only:
        u = User(username=account, following_date=datetime.date.today())
        db.session.add(u)
        db.session.commit()

    for account in follower_only:
        u = User(username=account, follower_date=datetime.date.today())
        db.session.add(u)
        db.session.commit()


if __name__ == "__main__":
    create_db()
    update_data()
