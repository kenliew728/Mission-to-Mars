from flask import Flask, render_template
from flask_pymongo import PyMongo
import scraping

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] ='mongodb+srv://kenliew:072879ken@cluster0.ddsko.mongodb.net/mars?retryWrites=true&w=majority'

#"mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Defining route for HTML Page
@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)

# Setting up "button" of the web application
@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   mars_data = scraping.scrape_all()
   mars.update({}, mars_data, upsert=True)
   return "Tesla Ready to Roll!"

if __name__ == "__main__":
    app.run(debug=True)