# Dependencies
from flask import Flask, render_template, redirect
import pymongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use pymongo to establish Mongo connection
conn= 'mongodb://localhost:27017/mars_info'
client = pymongo.MongoClient(conn)

db = client.mars_info

# Route that will trigger the scrape function
@app.route('/scrape')
def scrape():

    # Run the scrape function
    mars_data = scrape_mars.scrape()

    # Update the Mongo database using update and upsert=True
    db = client.mars_info
    db.mars_info.insert(mars_data)


    #Redirect back to home page
    #return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
    
