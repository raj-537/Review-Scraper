from logger_class import getLog

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import  Figure

from flask import Flask, render_template, url_for, request, Response, jsonify, redirect
from flask_cors import CORS, cross_origin
from flask import Markup

from mongoDBOperations import MongoDBManagement
from FlipkartScrapping import FlipkartScrapper

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

import threading
import io
import os

import pandas as pd
import numpy as np

import plotly.express as px
import json
import plotly



rows = {}

collection_name = None

logger = getLog('flipkart.py')

free_status = True

db_name = 'Flipkart-Scrapper'



#initialising Flask app
app = Flask(__name__)
#for selenium driver impelementaion on heroku
chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location  = os.environ.get('GOOGLE_CHOME_BIN')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('-no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--headless')
CORS(app=app)





#to avoid timeout issue on heroku

class threadClass:

    def __init__(self, searchString, scrapper_object):
        
        self.searchString = searchString
        self.scrapper_object = scrapper_object
        
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True  # Daemonize thread
        thread.start()  # Start the execution

    def run(self):
        global collection_name, free_status
        free_status = False
        collection_name = self.scrapper_object.getReviewsToDisplay(searchString=self.searchString, username='kj',password='Kymo007' )
        logger.info("Thread run completed")
        free_status = True


@app.route('/', methods=['POST', 'GET'])
@cross_origin()
def index():
    if request.method == 'POST':
        global free_status
        ## To maintain the internal server issue on heroku
        if free_status != True:
            return "This website is executing some process. Kindly try after some time..."
        else:
            free_status = True
        searchString = str(request.form['search']).replace(' ','')  # obtaining the search string entered in the form
        #expected_review = int(request.form['expected_review'])
        try:
            #review_count = 0
            responses = []
            scrapper_object = FlipkartScrapper(chrome_options=chrome_options)
            mongoClient = MongoDBManagement(username='kj', password='Kymo007')
            scrapper_object.openURL("https://www.flipkart.com/")
            logger.info("Url hitted")
            scrapper_object.login_popup_handle()
            logger.info("login popup handled")
            scrapper_object.searchProduct(search_string=searchString)
            logger.info(f"Search begins for {searchString}")
            if mongoClient.isCollectionPresent(collectionName=searchString, db_name=db_name):
                rows, mongo_client = mongoClient.findQueryOrAllRecords(db_name=db_name, collection_name=searchString)
                for row in rows:
                    responses.append([row])
                mongo_client.close()
                df_main = pd.DataFrame()
                for i in responses:
                    res  = scrapper_object.createDataFrameIncludingAllColumn(i[0])
                    df_main = pd.concat([df_main,res],ignore_index=True, verify_integrity=True)
                scrapper_object.saveDataFrameToFile(file_name="static/scrapper_data.csv", dataframe=df_main)
                # reviews = [i for i in response]
                # mongo_client.close()
                
                # #dataframe = scrapper_object.createDataFrameIncludingAllColumn(reviews)
                # scrapper_object.saveDataFrameToFile(file_name="static/scrapper_data.csv",
                #                                     dataframe=pd.DataFrame(reviews))
                logger.info("Data saved in scrapper file")
                # mongo_client.close()
                df_main['comments']
                df_main['offer_details']
                #scrapper_object.driver.close()
                return render_template('results.html', rows=Markup(df_main.to_html(index=False, classes="table table-bordered table-hover table-striped")))  # show the results to user
            else:
                
                threadClass(searchString=searchString,scrapper_object=scrapper_object)
                logger.info("data saved in scrapper file")
                #scrapper_object.driver.close()
                return redirect(url_for('feedback'))
            

        except Exception as e:
            raise Exception("(app.py) - Something went wrong while rendering all the details of product.\n" + str(e))

    else:
        return render_template('index.html')


@app.route('/feedback', methods=['GET'])
@cross_origin()
def feedback():
    try:
        global collection_name
        #collection_name = 'iphone13'
        response = []
        if collection_name is not None:
            scrapper_object = FlipkartScrapper()
            scrapper_object.driver.close()
            mongoClient = MongoDBManagement(username='kj', password='Kymo007')
            rows, mongo_client = mongoClient.findQueryOrAllRecords(db_name="Flipkart-Scrapper", collection_name=collection_name)
            for row in rows:
                response.append([row])
            mongo_client.close()
            df_main = pd.DataFrame()
            for i in response:
                res  = scrapper_object.createDataFrameIncludingAllColumn(i[0])
                df_main = pd.concat([df_main,res],ignore_index=True, verify_integrity=True)
            scrapper_object.saveDataFrameToFile(file_name="static/scrapper_data.csv", dataframe=df_main)
            collection_name = None
            
            #scrapper_object.driver.close()
            return render_template('results.html', rows=Markup(df_main.to_html(index=False, classes="table table-bordered table-hover table-striped")))
        else:
            #scrapper_object.driver.close()
            return render_template('results.html', rows=None)
    except Exception as e:
        raise Exception("(feedback) - Something went wrong on retrieving feedback.\n" + str(e))


@app.route("/graphs", methods=['GET'])
@cross_origin()
def graph():
    return redirect(url_for('plot_png'))


@app.route('/graph', methods=['GET'])
def plot_png():
    fig = create_figure()
    
    return render_template('graphs.html', jsonGraph = fig)


def create_figure():
    data = pd.read_csv("static/scrapper_data.csv")
    df = pd.DataFrame(data=data)
    fig = px.histogram(df, x='product_name', y='ratings', color='ratings')
    graphJson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJson

if __name__ == "__main__":
    app.run(port=8088, debug=True)  # running the app on the local machine on port 8000
