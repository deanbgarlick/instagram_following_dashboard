from app import app
import json
import os
from app.scraper import scrape_connected_accounts

@app.route("/")
def index():

    # Use os.getenv("key") to get environment variables
    app_name = os.getenv("APP_NAME")

    if app_name:
        return f"Hello from {app_name} running in a Docker container behind Nginx!"

    return "Hello from Flask"


@app.route("/scrape")
def selenium_function():
    followers, following = scrape_connected_accounts()
    with open('./network.json', 'w') as f:
        json.dump({'followers': followers, 'following': following}, f)
    return "Scraping complete"
