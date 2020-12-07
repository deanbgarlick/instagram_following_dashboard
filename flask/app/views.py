from app import app
import json
import os
from app.scraper import InstagramNetworkScraper
from app.update_data import update_users_in_db
from app import models, db
from app.models import User
import datetime

from flask import send_file, g

import pandas as pd
from sqlalchemy import create_engine
from flask import Flask, render_template


def get_db_engine():
    engine = getattr(g, '_database_engine', None)
    if engine is None:
        engine = g._database_engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    return engine


@app.route("/")
def index():

    app_name = os.getenv("APP_NAME")

    if app_name:
        return f"Hello from {app_name} running in a Docker container behind Nginx!"

    return "Hello from Flask"


@app.route("/scrape")
def selenium_function():
    update_users_in_db()
    return "Scraping complete"


@app.route('/getCSV') # this is a job for GET, not POST
def get_csv():
    engine = get_db_engine()
    df = pd.read_sql_table('user', engine)
    df.to_csv('./network.csv')
    return send_file('/home/dashboard/network.csv',
                     mimetype='text/csv',
                     attachment_filename='network.csv',
                     as_attachment=True)
