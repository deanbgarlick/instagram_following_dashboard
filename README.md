A simple containerized application to scrape the followers and following accounts for an instagram page. This was created to automate the collection of these lists for a Christmas present to a friend with a hobby crafts instagram page.

To spin up and run this application on a UNIX machine with docker clone this repo and then execute ```
sh entrypoint.sh``` in a terminal.

The app consists of a flask app behind a gunicorn server and nginx reverse proxy. The flask app contains functionality to scrape the instagram followers using selenium and allows for the results to be downloaded to csv from a webpage. The instagram follower data is stored and updated on a postgres db service spun up by docker-compose.