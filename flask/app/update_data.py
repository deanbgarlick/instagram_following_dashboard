import datetime
import json
from app import app
from app import db, models, scraper


def update_users_in_db():

    follower_accounts, following_accounts = scraper.InstagramNetworkScraper().scrape_connection_accounts(app.config['ACCOUNT_TO_SCRAPE'])

    for usernames, date_attribute in [(follower_accounts, 'follower_date'), (following_accounts, 'following_date')]:
        for username in usernames:
            account = models.User.query.filter_by(username=username).first()
            if account is None:
                u = models.User(username=username, **{date_attribute: datetime.date.today()})
                db.session.add(u)
                db.session.commit()
            else:
                if getattr(account, date_attribute) is None:
                    setattr(account, date_attribute, datetime.date.today())
                    db.session.commit()
                else:
                    pass
