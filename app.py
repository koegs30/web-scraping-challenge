from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
import pymongo

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars")

# Route that renders index.html
@app.route("/")
def index():
    mars = mongo.db.collection.find_one()
    return render_template("index.html", mars=mars)

# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():
    # Run scrape function
    mars = mongo.db.collection
    mars_data = scrape_mars.scrape()

    # Update the Mongo database
    mars.update({},mars_data,upsert=True)

    # Redirect back to home page
    return redirect("/",code=302)

if __name__ == "__main__":
    app.run(debug=True)