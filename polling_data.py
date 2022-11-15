import sqlite3

import matplotlib.pyplot as plt

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

    if approval_ratings:
        x_axis = dates
        y_axis = approval_ratings
        plt.plot(x_axis, y_axis, linestyle='--', marker='o', color='g', label='average approval rating/day with marker')
        for index in range(len(x_axis)):
            ax.text(x_axis[index], y_axis[index], y_axis[index], size=12)

    if disapproval_ratings:
        x_axis = dates
        y_axis = disapproval_ratings
        plt.plot(x_axis, y_axis, linestyle='--', marker='o', color='r', label='average approval rating/day with marker')
        for index in range(len(x_axis)):
            ax.text(x_axis[index], y_axis[index], y_axis[index], size=12)

    plt.savefig('./static/images/' + img_name + '.png')
