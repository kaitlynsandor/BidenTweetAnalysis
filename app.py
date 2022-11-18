import os
import sqlite3

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
import matplotlib
from word_cloud import *
from polling_data import *
sw_spacy = []
# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/insights", methods=["GET", "POST"])
def insights():
    list_of_words = get_tweets_date_range('11/24/2021', '12/21/2021', sw_spacy)
    create_save_word_cloud_from_dirty_tweets(list_of_words, 'cloud')
    output = get_dates_and_approval('11/24/2021', '12/21/2021')
    graph_and_save_results(output[0], output[1], output[2], 'polling_data', "11/24/2021 --> 12/21/2021")
    generate_complex_sql()
    return render_template('insights.html')

@app.route("/about",  methods=["GET", "POST"])
def about():
    return render_template('about.html')

@app.route('/submitqueries')
def form():
    return render_template('submitqueries.html')
 
@app.route('/data/', methods = ['POST', 'GET'])
def data():
    if request.method == 'GET':
        return f"The URL /data is accessed directly. Try going to '/form' to submit form"
    if request.method == 'POST':
        form_data = request.form
        query = str(request.form.get("Your Query"))
        print(query)

        try:
            con = sqlite3.connect("data.db")
            cursor_object = con.cursor()

            execution_result = cursor_object.execute(query)
            result = []

            for i in execution_result:
                result.append(i)

            # get structure of output, print out an output table

        except:
            result = "error with query"

        return render_template('data.html',form_data = form_data, result = result)

if __name__=="__main__":
    matplotlib.use('Agg')
    en = spacy.load('en_core_web_sm')
    sw_spacy = en.Defaults.stop_words
    app.run(host=os.getenv('IP', '0.0.0.0'),
            port=int(os.getenv('PORT', 8000)))