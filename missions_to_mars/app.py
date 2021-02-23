from flask import Flask, render_template, redirect, url_for
from pymongo import MongoClient
import scrape_mars as scrape_mars
from flask_pymongo import PyMongo

#missions_to_mars\scrape_mars.py
# Imports and dependencies


app = Flask(__name__)
# Use flask_pymongo to set up mongo connection
# Use pymongo to set up mongo connection

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")

# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")
# @app.route("/")
# def index():
#     mars_db = client.mars_db
#     data = mars_db.summary_data.find_one()
#     return render_template("index.html", data=data, current_time=datetime.utcnow())



@app.route("/")
def index():
    mars = mongo.db.collection.find_one()
    return render_template("index.html", mars=mars, images=mars['mars_images'])



@app.route("/scrape")
def scrape_all():

    mars_data = scrape_mars.scrape()
    mongo.db.collection.update({}, mars_data, upsert=True)
#    mongo.update({}, mars_data, upsert=True)
    return redirect('/', code=302)

if __name__ == "__main__":
    app.run(debug=True)