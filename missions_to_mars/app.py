from flask import Flask, render_template, redirect, url_for

from pymongo import MongoClient
import missions_to_mars.scrape_mars2 as scrape_mars

#missions_to_mars\scrape_mars.py
# Imports and dependencies
from bs4 import BeautifulSoup
import requests
import os
from splinter import Browser
import pymongo
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from datetime import datetime

app = Flask(__name__)
# Use flask_pymongo to set up mongo connection
# Use pymongo to set up mongo connection
mongo_url = "mongodb://localhost:27017"
client = MongoClient(mongo_url)
db = client.mars


# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")
@app.route("/")
def index():
    mars_db = client.mars_db
    data = mars_db.summary_data.find_one()
    return render_template("index.html", data=data, current_time=datetime.utcnow())



# @app.route("/")
# def index():
#     mars = db
#     return render_template("index.html", mars=mars)

def scrape_data():
    scraped_data = scrape_mars.scrape()
    mars_db = client.mars_db
    data = mars_db.summary_data
    data.delete_many({})
    data.insert(scraped_data)
    return redirect("/", code=302)


# @app.route("/scrape")
# def scrape_all():
#     mars = db
#     mars_data = scrape_mars.scrape_all()
#     mars.update({}, mars_data, upsert=True)
#     return redirect('/', code=302)

if __name__ == "__main__":
    app.run(debug=True)