import sqlite3
import matplotlib.pyplot as plt
from nltk.probability import FreqDist
from wordcloud import WordCloud
import requests
from nltk.corpus import stopwords
import string

def get_test_words():
    response = requests.get(
        'https://www.mit.edu/~ecprice/wordlist.10000',
        timeout=10)
    string_of_words = response.content.decode('utf-8')
    return string_of_words.splitlines()

def bad_word(word):
    stop_words = stopwords.words("english")
    if word not in stop_words:
        return False
    return True

def get_tweets_date_range(start_date, end_date):
    con = sqlite3.connect("data.db")
    cursor_object = con.cursor()
    query = "SELECT tweet FROM tweets WHERE timestamp BETWEEN " + "'" + start_date + "'" + " AND " + "'" + end_date + "'"
    execution_result = cursor_object.execute(query)
    tweets = []
    for tweet in execution_result:
        for word in tweet[0].split(' '):
            word = word.lower()
            new_word = word.translate(str.maketrans('', '', string.punctuation))
            new_word = new_word.replace("’", '')
            if len(word) > 1 and new_word == word and not bad_word(word):
                tweets.append(word)
    return tweets

def get_num_topics(tweets):
    return 30

def get_frequency_dict(tweets, topics):
    flat_words = []
    for tweet in tweets:
        flat_words.append(tweet)

    word_freq = FreqDist(flat_words)
    word_freq.most_common(30)

    # retrieve word and count from FreqDist tuples
    most_common_count = [x[1] for x in word_freq.most_common(30)]
    most_common_word = [x[0] for x in word_freq.most_common(30)]

    # create dictionary mapping of word count
    return dict(zip(most_common_word, most_common_count))


def generate_and_save_cloud(dictionary,
                            img_name):  # Create Word Cloud of top 30 words..need to figure out best number of topics to generate given a tweet
    wordcloud = WordCloud(colormap='Accent', background_color='black') \
        .generate_from_frequencies(dictionary)

    # plot with matplotlib
    plt.figure(figsize=(12, 8))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.savefig('./static/images/' + img_name + '.png')

def create_save_word_cloud_from_dirty_tweets(tweets, img_name):
    num_topics = get_num_topics(tweets)
    dictionary = get_frequency_dict(tweets, num_topics)
    generate_and_save_cloud(dictionary, img_name)