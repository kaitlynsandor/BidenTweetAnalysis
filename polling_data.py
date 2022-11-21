import sqlite3
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

def get_dates_and_approval(first_date=None, second_date=None):
    con = sqlite3.connect("data.db")
    cursor_object = con.cursor()
    query = "SELECT startdate, approve, disapprove FROM polling_data WHERE startdate BETWEEN " + "'" + first_date + "'" + " AND " + "'" + second_date + "'"

    execution_result = cursor_object.execute(query)
    dates_to_rating = {}

    for i in execution_result:
        if i[0] not in dates_to_rating.keys():
            dates_to_rating[i[0]] = (float(i[1]), float(i[2]), 1)
        else:
            new_approval = float(i[1])
            new_disapproval = float(i[2])
            old_stats = dates_to_rating[i[0]]
            dates_to_rating[i[0]] = ((old_stats[0]*old_stats[2]+new_approval)/(old_stats[2]+ 1),
                                     (old_stats[1]*old_stats[2]+new_disapproval)/(old_stats[2]+ 1),
                                     old_stats[2]+1)
        dates = []
        approval = []
        disapproval = []
        for key in dates_to_rating.keys():
            dates.append(key)
            approval.append(dates_to_rating[key][0])
            disapproval.append(dates_to_rating[key][1])
    return dates, approval, disapproval

def graph_and_save_results(dates, approval_ratings, disapproval_ratings, img_name, date_range):

    fig, ax = plt.subplots(figsize=(12, 8))
    plt.title('Ratings for Date Range: ' + date_range)
    plt.xlabel('Days')
    plt.ylabel('Rating % (Green Approval/Red Disapproval)')

    myLocator = mticker.MultipleLocator(4)
    ax.xaxis.set_major_locator(myLocator)

    if approval_ratings:
        x_axis = dates
        y_axis = approval_ratings
        plt.plot(x_axis, y_axis, linestyle='--', marker='o', color='g', label='average approval rating/day with marker')
        for index in range(len(x_axis)):
            ax.text(x_axis[index], round(y_axis[index], 1), round(y_axis[index], 1), size=12)

    if disapproval_ratings:
        x_axis = dates
        y_axis = disapproval_ratings
        plt.plot(x_axis, y_axis, linestyle='--', marker='o', color='r', label='average approval rating/day with marker')
        for index in range(len(x_axis)):
            ax.text(x_axis[index], round(y_axis[index], 1), round(y_axis[index], 1), size=12)

    plt.savefig('./static/images/' + img_name + '.png')

def generate_complex_sql():
    con = sqlite3.connect("data.db")
    cursor_object = con.cursor()
    query = "SELECT DISTINCT startdate, average_tweet_likes, average_approve FROM((SELECT t1.tweet_date, t1.average_tweet_likes FROM (SELECT tweet_date,AVG(Cast(tweet_like_count as Float)) as average_tweet_likes FROM tweets GROUP BY tweet_date \
                    HAVING COUNT(*) > 1) t1 \
                    JOIN tweets t2 ON t1.tweet_date = t2.tweet_date) average_tweets \
               LEFT JOIN \
                 (SELECT t3.startdate, t3.average_approve \
                 FROM \
                    ( \
                      (SELECT startdate,AVG(Cast(approve as Float)) as average_approve \
                        FROM polling_data GROUP BY startdate \
                        HAVING COUNT(*) > 1) t3 \
                    JOIN polling_data t4 ON t3.startdate=t4.startdate) \
                ) \
                average_polls \
                ON average_polls.startdate=average_tweets.tweet_date \
             ) \
             WHERE average_approve is not NULL \
             AND average_tweet_likes IS NOT NULL"
    execution_result = cursor_object.execute(query)

    dates = []
    approval_ratings = []
    likes = []

    for i in execution_result:
        dates.append(i[0])
        likes.append(i[1])
        approval_ratings.append(i[2])

    fig, ax = plt.subplots(figsize=(12, 8))
    ax2 = ax.twinx()

    plt.title('Average Approval Rating and Average Likes/Tweet Over Time')
    plt.xlabel('Days')
    ax.set_ylabel('Average Rating %')
    ax2.set_ylabel("Average Likes/Day")

    myLocator = mticker.MultipleLocator(5)
    ax.xaxis.set_major_locator(myLocator)
    ax2.xaxis.set_major_locator(myLocator)

    x_axis = dates
    y_axis = approval_ratings
    ax.plot(x_axis, y_axis, linestyle='--', marker='o', color='g', label='average approval rating/day with marker')
    for index in range(len(x_axis)):
        ax.text(x_axis[index], round(y_axis[index], 1), round(y_axis[index], 1), size=9)

    y_axis = likes
    ax2.plot(x_axis, y_axis, linestyle='--', marker='o', color='purple', label='average likes/day with marker')
    for index in range(len(x_axis)):
        ax2.text(x_axis[index], round(y_axis[index], 1), round(y_axis[index], 1), size=9)


    plt.savefig('./static/images/' + 'ratings' + '.png')






