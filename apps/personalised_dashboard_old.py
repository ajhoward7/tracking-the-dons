import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from datetime import *
import polyline
import os
from flask_caching import Cache
import uuid

from app import app

from plotly_plotting import preprocess_activities
from df_preprocessing import df_preprocessing

#######################################################################################################################

mapbox_access_token = 'pk.eyJ1IjoiamFja2x1byIsImEiOiJjajNlcnh3MzEwMHZtMzNueGw3NWw5ZXF5In0.fk8k06T96Ml9CLGgKmk81w'
days_dict = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}


#######################################################################################################################

cache = Cache(app.server, config={
    'CACHE_TYPE': 'redis',
    # Note that filesystem cache doesn't work on systems with ephemeral
    # filesystems like Heroku.
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': 'cache-directory',

    # should be equal to maximum number of users on the app at a single time
    # higher numbers will store more data in the filesystem / redis cache
    'CACHE_THRESHOLD': 200
})

def get_dataframe(session_id):
    @cache.memoize()
    def query_and_serialize_data(session_id):

        user_files = os.listdir('../users/')
        number_str = [str(x) for x in range(10)]
        user_files = [file for file in user_files if file[0] in number_str]
        user_files.sort()
        latest_user = user_files[0]

        activities_df = preprocess_activities(latest_user)

        by_week_df = df_preprocessing(activities_df)

        return activities_df, by_week_df

    return query_and_serialize_data(session_id)


#######################################################################################################################
def serve_layout():
    session_id = str(uuid.uuid4())
    activities_df, by_week_df = get_dataframe(session_id)

    layout = html.Div([
        html.Div([
            html.H2("Tracking the Dons - Alex")
        ], className='banner'),

        html.Div(dcc.Slider(
            id='crossfilter-year--slider-2',
            min=activities_df['year'].min(),
            max=activities_df['year'].max(),
            value=activities_df['year'].max(),
            step=None,
            marks={str(year): str(year) for year in activities_df['year'].unique()}
        ), style={'width': '45%', 'padding': '0px 30px 30px 30px'}),

        html.Div(
            className="row",
            children=[
                html.Div(
                    className="six columns",
                    children=[
                        html.Div(
                            children=dcc.Graph(
                                id='crossfilter-indicator-scatter-2',
                                hoverData={'points': [{'customdata': list(activities_df.id)[0]}]}
                            )
                        ),
                        html.Div(className='row',
                                 children = [
                                                html.Div(
                                                className="six columns",
                                                children=[dcc.Graph(id='miles-hist-2')]),
                                                html.Div(className="six columns",
                                                children=[dcc.Graph(id='weekly-mileage-2')])]



                        )
                    ]
                ),
                html.Div(
                    className="six columns",
                    children=html.Div([
                        dcc.Graph(
                            id='parallel-2'
                        ),
                        dcc.Graph(
                            id='run-geo-2'
                        ),
                        dcc.Graph(id='weekly-mileage-2')

                    ])
                )
            ]
        )
    ])

    return layout

layout = serve_layout()


#######################################################################################################################

@app.callback(
    dash.dependencies.Output('crossfilter-indicator-scatter-2', 'figure'),
    [dash.dependencies.Input('crossfilter-year--slider-2', 'value')])
def update_graph_2(year_value):

    session_id = str(uuid.uuid4())
    activities_df, by_week_df = get_dataframe(session_id)

    df2 = activities_df[activities_df['year'] == year_value]

    sizeref = 20 * max(activities_df['size']) / (100 ** 2)
    data = []
    for run_type in ['Run', 'Workout', 'Long Run', 'Race']:
        trace = go.Scatter(
            x=df2['miles'][df2['workout_type'] == run_type],
            y=df2['pace_mile'][df2['workout_type'] == run_type],
            mode='markers',
            hoverinfo='text',
            opacity=0.8,
            name=run_type,
            customdata=df2['id'][df2['workout_type']==run_type],
            hovertext=df2['text'][df2['workout_type'] == run_type],
            marker=dict(
                symbol='circle',
                sizemode='area',
                sizeref=sizeref,
                size=df2['size'][df2['workout_type'] == run_type],
                line=dict(
                    width=2
                ),
            )
        )
        data.append(trace)

    layout = go.Layout(
        title='Run Summary',
        hovermode='closest',
        xaxis=dict(
            title='Distance (Miles)',
            gridcolor='rgb(255, 255, 255)',
            range=[0, 20],
            zerolinewidth=1,
            ticklen=5,
            gridwidth=2,
        ),
        yaxis=dict(
            title='Pace (Seconds per Mile)',
            gridcolor='rgb(255, 255, 255)',
            range=[0, 600],
            zerolinewidth=1,
            ticklen=5,
            gridwidth=2,
        ),
        paper_bgcolor='rgb(243, 243, 243)',
        plot_bgcolor='rgb(243, 243, 243)',
        autosize=False
    )

    return {'data':data, 'layout':layout}


def create_time_series_2(this_week, title):
    days_dict = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
    this_week = this_week.sort_values(['day'], ascending = True)
    this_week.day = this_week.day.apply(lambda x : days_dict[x])
    custom_colours = {'Run': 'blue', 'Workout':'orange', 'Race':'red', 'Long Run':'green'}

    data = []
    for day in days_dict.values():
        data.append(go.Bar(
            orientation = 'h',
            y=[day],
            x=[0],
            marker=dict(opacity=[0])))

    for index, row in this_week.iterrows():
        data.append(go.Bar(
            orientation = 'h',
            y=[row['day']],
            x=[row['miles']],
            marker=dict(color=[custom_colours[row['workout_type']]],
                        opacity = [0.75]),
            hovertext=[row['text']],
            hoverinfo = 'text'))



    layout = dict(
        hovermode='closest',
        barmode='stack',
        title=title,
        autosize=False,
        showlegend=False
        )

    return {'data': data, 'layout':layout}


@app.callback(
    dash.dependencies.Output('weekly-mileage-2', 'figure'),
    [dash.dependencies.Input('crossfilter-indicator-scatter-2', 'hoverData')])

def update_mileage_2(hoverData):
    session_id = str(uuid.uuid4())
    activities_df, by_week_df = get_dataframe(session_id)

    id = hoverData['points'][0]['customdata']
    activity = activities_df[activities_df.id == id]
    date = list(pd.to_datetime(activity.date))[0]
    week_start = date - timedelta(days=date.weekday())
    week_end = week_start + timedelta(days=6)
    this_week = activities_df[activities_df.week_start == week_start]

    this_week['day'] = this_week.date.apply(lambda x: x.weekday())
    total_miles = this_week.miles.sum()
    title = '<b>{} - {}</b><br>Total Miles: {}'.format(week_start.date(), week_end.date(), int(total_miles))

    return create_time_series_2(this_week, title)


def create_geo_2(summary_polyline):
    gps = polyline.decode(summary_polyline)
    df = pd.DataFrame(gps, columns=['lat', 'long'])
    df['cnt'] = 1

    data = go.Data([
        go.Scattermapbox(
            lat=df.lat,
            lon=df.long,
            mode='lines',
            marker=go.Marker(
                size=17,
                color='rgb(255, 0, 0)',
                opacity=0.7
            )
        )])

    layout = go.Layout(
        autosize=False,
        hovermode='closest',
        showlegend=False,
        mapbox=dict(
            accesstoken=mapbox_access_token,
            bearing=0,
            center=dict(
                lat=df.lat[int(len(df)/4)],
                lon=df.long[int(len(df)/4)]
            ),
            pitch=0,
            zoom=10.5,
            style='light'
        ),
    )

    fig = dict(data=data, layout=layout)

    return fig


@app.callback(
    dash.dependencies.Output('run-geo-2', 'figure'),
    [dash.dependencies.Input('crossfilter-indicator-scatter-2', 'hoverData')])
def update_geo_2(hoverData):
    session_id = str(uuid.uuid4())
    activities_df, by_week_df = get_dataframe(session_id)
    id = hoverData['points'][0]['customdata']
    summary_polyline = list(activities_df[activities_df.id==id]['map.summary_polyline'])[0]

    return create_geo_2(summary_polyline)


def create_parallel_2(by_week_df_2):
    session_id = str(uuid.uuid4())
    activities_df, by_week_df = get_dataframe(session_id)
    dimensions = []
    for i in range(7):
        dimensions.append(
            dict(range=[0, 20],
                 label='{}'.format(days_dict[i]), values=by_week_df_2['miles_{}'.format(i)]))

    data = [
        go.Parcoords(
            line=dict(color=by_week_df['miles'],
                      colorscale='Hot',
                      showscale=True,
                      reversescale=True),
            opacity=0.5,
            dimensions=dimensions, hoverinfo='text')

    ]

    layout = go.Layout(
        plot_bgcolor='#E5E5E5',
        paper_bgcolor='#E5E5E5',
        title='Miles per week broken down by day'
    )

    return go.Figure(data=data, layout=layout)



@app.callback(
    dash.dependencies.Output('parallel-2', 'figure'),
    [dash.dependencies.Input('crossfilter-year--slider-2', 'value')])
def update_parallel_2(year_value):
    session_id = str(uuid.uuid4())
    activities_df, by_week_df = get_dataframe(session_id)
    by_week_df_2 = by_week_df[by_week_df.year==year_value]

    return create_parallel_2(by_week_df_2)


def create_distance_hist_2(all_miles, this_miles):
    trace1 = go.Histogram(

        x=all_miles[(all_miles >= this_miles-0.5)&(all_miles < this_miles + 0.5)],
        hoverinfo='text'
    )
    trace0 = go.Histogram(
        x=all_miles[(all_miles < this_miles-0.5)|(all_miles >= this_miles + 0.5)],
        hoverinfo='text'
    )
    data = [trace0, trace1]
    layout = go.Layout(barmode='stack',
                       showlegend=False,
                       bargap=0.2)
    return go.Figure(data=data, layout=layout)


@app.callback(
    dash.dependencies.Output('miles-hist-2', 'figure'),
    [dash.dependencies.Input('crossfilter-indicator-scatter-2', 'hoverData')])
def update_distance_hist_2(hoverData):
    session_id = str(uuid.uuid4())
    activities_df, by_week_df = get_dataframe(session_id)

    id = hoverData['points'][0]['customdata']
    activity = activities_df[activities_df.id == id]
    year = list(activity.year)[0]
    all_miles = activities_df[activities_df.year==year]['miles'].apply(lambda x : round(x))
    this_miles = int(list(activity['miles'])[0])

    return create_distance_hist_2(all_miles, this_miles)
