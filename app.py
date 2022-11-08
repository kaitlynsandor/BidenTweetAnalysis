import os
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from nltk.probability import FreqDist
from wordcloud import WordCloud
import matplotlib as plt

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

@app.route("/about",  methods=["GET", "POST"])
def about():
    return render_template('about.html')

def get_topic_frequency(tweets):
    # iterate through each tweet, then each token in each tweet, and store in one list
    flat_words = [item for sublist in tweets for item in sublist]
    word_freq = FreqDist(flat_words)
    word_freq.most_common(30)

    # retrieve word and count from FreqDist tuples

    most_common_count = [x[1] for x in word_freq.most_common(30)]
    most_common_word = [x[0] for x in word_freq.most_common(30)]

    # create dictionary mapping of word count
    top_30_dictionary = dict(zip(most_common_word, most_common_count))

    # Create Word Cloud of top 30 words
    wordcloud = WordCloud(colormap='Accent', background_color='black') \
        .generate_from_frequencies(top_30_dictionary)

    # plot with matplotlib
    plt.figure(figsize=(12, 8))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.savefig('top_30_cloud.png')
    plt.show()


if __name__=="__main__":
    app.run(host=os.getenv('IP', '0.0.0.0'),
            port=int(os.getenv('PORT', 8000)))