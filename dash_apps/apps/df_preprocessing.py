import pandas as pd
from datetime import *

def df_preprocessing(activities_df):

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

    return by_week_df