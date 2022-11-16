import pandas as pd
import sqlite3

# sameple code to read in csv to database once we get to this stage...this code only needs to be run once
with open('BidenTweetsFinal.csv', 'r') as f:
    con = sqlite3.connect("../data.db")
    cursor_object = con.cursor()

    df = pd.read_csv('BidenTweetsFinal.csv')
    df.columns = df.columns.str.strip()
    df.to_sql("tweets", con)

    df = pd.read_csv('PollingFinal.csv')
    df.columns = df.columns.str.strip()
    df.to_sql("polling_data", con)