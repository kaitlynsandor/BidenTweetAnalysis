import matplotlib.pyplot as plt
from nltk.probability import FreqDist
from wordcloud import WordCloud
import requests

def get_test_words():
    response = requests.get(
        'https://www.mit.edu/~ecprice/wordlist.10000',
        timeout=10)
    string_of_words = response.content.decode('utf-8')
    string_of_words.splitlines()

def clean_tweets(tweets):
    pass

def get_num_topics(tweets):
    return 30

def get_frequency_dict(tweets, topics):
    # iterate through each tweet, then each token in each tweet, and store in one list
    # flat_words = [item for sublist in tweets for item in sublist]

    word_freq = FreqDist(tweets)
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
    clean_tweets(tweets)
    dictionary = get_frequency_dict(tweets, num_topics)
    generate_and_save_cloud(dictionary, img_name)