import pandas as pd
import numpy as np
import datetime
import re

# convert to dataframes
biden_tweets_df = pd.read_csv('data_cleaning/JoeBidenTweets.csv')
polling_df = pd.read_csv('data_cleaning/polling_data.csv')

# drop unnecessary columns
biden_tweets_df = biden_tweets_df.drop(['url'], axis = 1)
polling_df = polling_df.drop(['subgroup', 'enddate', 'url', 'president'], axis = 1)

# split the date and the time in biden_tweets_df
new = biden_tweets_df["timestamp"].str.split(" ", n = 1, expand = True)
biden_tweets_df["timestamp"]= new[0]

# convert timestamps
def timestamps():
    i = 0
    for t in biden_tweets_df["timestamp"]:
        biden_tweets_df["timestamp"].loc[i] = datetime.datetime.strptime(t, '%Y-%m-%d').strftime("%m/%d/%Y")
        i += 1

# delete links in tweets
def delete_urls():
    i = 0
    for tweet in biden_tweets_df["tweet"]:
        biden_tweets_df["tweet"].loc[i] = re.sub(r'http:\S+', '', tweet)
        i += 1

#testing
timestamps()
delete_urls()
print(biden_tweets_df["timestamp"][0])
print(biden_tweets_df["timestamp"][88])
print(biden_tweets_df["timestamp"][100])
print(biden_tweets_df["tweet"][100])

# export csvs
biden_tweets_df.to_csv(r'BidenTweetsFinal.csv')
polling_df.to_csv(r'PollingFinal.csv')
