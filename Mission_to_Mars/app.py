from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

conn = "mongodb://localhost:27017"
mongo = PyMongo(app, uri="mongodb://localhost:27017/scrape_mars_app")

@app.route("/")
def home():

    mars_data = mongo.db.collection.find_one()
    return render_template("index.html", mars=mars_data)

@app.route("/scrape")
def scrape():
    
    mars_dict = scrape_mars.scrape()
    mongo.db.collection.update({}, mars_dict, upsert=True)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)



