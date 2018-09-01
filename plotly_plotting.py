import pandas as pd
from pandas.io.json import json_normalize
from datetime import *
import numpy as np
import math
import json

metres_mile = 1609.34
workout_type_dict = {0:'Run',1:'Race',2:'Long Run',3:'Workout'}
days_dict = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}


def preprocess_activities(username):

    data = json.load(open('users/{}/activities.json'.format(username)))
    activities_df = json_normalize(data)


    activities_df = activities_df[
        ['average_speed', 'distance', 'moving_time', 'name', 'start_date_local', 'id', 'workout_type', 'type',
         'map.summary_polyline']]
    activities_df = activities_df[activities_df.type == 'Run']

    activities_df['pace_mile'] = metres_mile / activities_df.average_speed
    activities_df['pace_km'] = 1000 / activities_df.average_speed

    activities_df['date'] = pd.to_datetime(activities_df.start_date_local.apply(lambda x: x.split('T')[0]))
    activities_df.drop(['average_speed', 'start_date_local', 'type'], axis=1, inplace=True)

    activities_df.workout_type = activities_df.workout_type.fillna(0)
    activities_df.workout_type = activities_df.workout_type.apply(lambda x: workout_type_dict[x])

    activities_df['miles'] = activities_df.distance / metres_mile
    activities_df['Distance (Kilometres)'] = activities_df.distance / 1000

    activities_df['size'] = activities_df.moving_time.astype('float').apply(lambda x: math.sqrt(x))
    activities_df['year'] = activities_df.date.apply(lambda x: x.year)

    activities_text = []
    for i in range(len(activities_df)):
        row = activities_df.iloc[i,]
        activities_text.append('{}<br>{}<br>'.format(row['name'].encode('ascii', 'ignore'),
                                                     row['date'].date()) + '{:.1f} miles<br>{:.2f} seconds/mile'.format(
            row['miles'], row['pace_mile']))

    activities_df['text'] = activities_text
    activities_df['week_start'] = activities_df.date.apply(lambda x : x - timedelta(days=x.weekday()))
    return activities_df


def group_df(activities_df):

    activities_grouped_df = activities_df.groupby(['date'], as_index=False)['miles'].sum()
    activities_grouped_df['dow'] = activities_grouped_df.date.apply(lambda x: x.weekday())
    activities_grouped_df['week_start'] = activities_grouped_df.date.apply(lambda x: x - timedelta(days=x.weekday()))

    miles_per_week = activities_grouped_df.groupby(['week_start'], as_index=False).miles.sum()
    by_week_df = pd.DataFrame(activities_grouped_df.week_start.unique(), columns=['week_start'])
    by_week_df['miles'] = 0

    for i in range(7):
        by_week_df['{}'.format(i)] = i

    for i in range(7):
        by_week_df = pd.merge(by_week_df, activities_grouped_df, left_on=['week_start', '{}'.format(i)],
                              right_on=['week_start', 'dow'], how='left', suffixes=('', '_{}'.format(i)))

    by_week_df = by_week_df[['week_start', 'miles_0', 'miles_1', 'miles_2', 'miles_3', 'miles_4', 'miles_5', 'miles_6']]
    by_week_df['year'] = by_week_df['week_start'].apply(lambda x: x.year)
    by_week_df.fillna(0, inplace=True)
    by_week_df = pd.merge(by_week_df, miles_per_week, how='left', on='week_start')

    return activities_grouped_df, by_week_df


def group_df_2(activities_df):

    activities_grouped_df_2 = activities_df.groupby(['workout_type', 'week_start'], as_index=False)['miles'].sum()

    by_week_activity_df = pd.DataFrame(activities_grouped_df_2.week_start.unique(), columns=['week_start'])

    for i in activities_df.workout_type.unique():
        by_week_activity_df['{}'.format(i)] = i

    by_week_activity_df['miles'] = 0

    activity_types = activities_df.workout_type.unique()
    n_activity_types = len(activity_types)
    for i in range(n_activity_types):
        by_week_activity_df = pd.merge(by_week_activity_df, activities_grouped_df_2,
                                       left_on=['week_start', '{}'.format(activity_types[i])],
                                       right_on=['week_start', 'workout_type'], how='left',
                                       suffixes=('', '_{}'.format(activity_types[i])))

    if 'miles_Long Run' not in by_week_activity_df.columns:
        by_week_activity_df['miles_Long Run'] = 0

    if 'miles_Workout' not in by_week_activity_df.columns:
        by_week_activity_df['miles_Workout'] = 0

    if 'miles_Run' not in by_week_activity_df.columns:
        by_week_activity_df['miles_Run'] = 0

    if 'miles_Race' not in by_week_activity_df.columns:
        by_week_activity_df['miles_Race'] = 0

    by_week_activity_df.fillna(0, inplace=True)

    by_week_activity_df['miles_Run'] = np.array(by_week_activity_df['miles_Run']) + np.array(
        by_week_activity_df['miles_Long Run'])

    return activities_grouped_df_2, by_week_activity_df


# def plot_charts(username):
#
#     activities_df = preprocess_activities(username)
#
#     chart_1 = chart_1_scatter.chart_plot(activities_df)
#
#     activities_grouped_df, by_week_df = group_df(activities_df)
#
#     chart_2 = chart_2_parallel.chart_plot(by_week_df)
#
#     activities_df['week_start'] = activities_df.date.apply(lambda x: x - timedelta(days=x.weekday()))
#
#     activities_grouped_df_2, by_week_activity_df = group_df_2(activities_df)
#
#     chart_3 = chart_3_bar.chart_plot(by_week_activity_df)
#
#     return(chart_1, chart_2, chart_3)




