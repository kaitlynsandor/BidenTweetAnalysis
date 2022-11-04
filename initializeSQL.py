import pandas as pd
import sqlite3


# sameple code to read in csv to database once we get to this stage...this code only needs to be run once
with open('tweets.csv', 'r') as f:
    con = sqlite3.connect("data.db")
    cursor_object = con.cursor()
    df = pd.read_csv('tweets.csv')
    df.columns = df.columns.str.strip()
    df.columns = df.columns.str.replace('.','')
    df.to_sql("tweets", con)

    df = pd.read_csv('tweets.csv')
    df.columns = df.columns.str.strip()
    df.columns = df.columns.str.replace('.', '')
    df.to_sql("tweets", con)