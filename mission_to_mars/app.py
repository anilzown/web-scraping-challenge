# from mission_to_mars.scrape_mars import scrape
# from scrape_mars_old import scrape
from scrape_mars import scrape
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
# import scrape_mars_old
# import pymongo

app = Flask(__name__)


mongo=PyMongo(app, uri="mongodb://localhost:27017/scrape_mars")
print("the db connection is establisehd ")


@app.route("/")
def home():
    destination_data=mongo.db.collection.find_one()
    return render_template("index.html", scrape_mars=destination_data)


@app.route("/scrape")
def scraper():
    mars_dict = scrape_mars.scrape()
    print (mars_dict)
    mongo.db.collection.update({}, mars_dict,upsert=True)
    # mars_dict = scrape_mars.scrape()
    # mongo.db.collection.update({}, mars_dict,upsert=True)
    return redirect("/")

if __name__=="__main__":
    app.run(debug=True)