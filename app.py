from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

#Use PyMongo to establish Mango connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():
    mars_data = mongo.db.mars_data.find_one()
    return render_template("index.html", mars_data = mars_data)

@app.route("/scrape")
def scraper():
    #make new collection "mars_data" in mars_app database
    mars_data = mongo.db.mars_data
    mars_info = scrape_mars.scrape()
    mars_data.update({}, mars_info, upsert=True)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
