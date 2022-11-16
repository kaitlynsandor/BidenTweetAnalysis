import pandas as pd
import numpy as np
import datetime
import re

# convert to dataframes
biden_tweets_df = pd.read_csv('data_cleaning/tweets_of_joe_biden.csv')
polling_df = pd.read_csv('data_cleaning/polling_data.csv')

# drop unnecessary columns
biden_tweets_df = biden_tweets_df.drop(['tweet_url'], axis = 1)
polling_df = polling_df.drop(['subgroup', 'enddate', 'url', 'president'], axis = 1)

# split the date and the time in biden_tweets_df
new = biden_tweets_df["tweet_date"].str.split(" ", n = 1, expand = True)
biden_tweets_df["tweet_date"]= new[0]

# convert timestamps
def timestamps():
    i = 0
    for t in biden_tweets_df["tweet_date"]:
        biden_tweets_df["tweet_date"].loc[i] = datetime.datetime.strptime(t, '%Y-%m-%d').strftime("%m/%d/%Y")
        i += 1

# delete links in tweets
def delete_urls():
    i = 0
    for tweet in biden_tweets_df["tweet_content"]:
        biden_tweets_df["tweet_content"].loc[i] = re.sub(r'http:\S+', '', tweet)
        i += 1

#testing
timestamps()
delete_urls()
print(biden_tweets_df["tweet_date"][0])
print(biden_tweets_df["tweet_date"][88])
print(biden_tweets_df["tweet_date"][100])
print(biden_tweets_df["tweet_content"][100])

# export csvs
biden_tweets_df.to_csv(r'BidenTweetsFinal.csv')
polling_df.to_csv(r'PollingFinal.csv')