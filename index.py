import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from plotly_plotting import preprocess_activities
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from datetime import *

from apps import alex_dashboard, personalised_dashboard
from app import app, server

from flask import Flask, redirect, render_template, url_for, flash, request

from scrape import scrape_activities
from credentials import client_id, client_secret
import requests
import json

redirect_url = 'https://www.strava.com/oauth/authorize?response_type=code&redirect_uri=http%3A%2F%2F35.164.243.185%2Fauthorize&client_id=20812'

wsgi_app = server.wsgi_app

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})


@server.route('/')
def home():
    return render_template('index.html', strava_url=redirect_url)


@server.route('/authorize', methods=('GET','POST'))
def authorize():
    code = request.args.get('code')
    r = requests.post('https://www.strava.com/oauth/token', data={'client_id':client_id, 'client_secret':client_secret, 'code':code})
    json_data = json.loads(r._content)
    access_token = json_data["access_token"]
    username = scrape_activities(access_token)

    ip = '127.0.0.1:5000'

    return redirect('http://{}/{}'.format(ip,username))


@server.route('/geo', methods=('GET','POST'))
def show_geo_vis():

    return "This is Taylor's part"


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/dashboard/alex':
        return alex_dashboard.layout
    elif pathname != None:
        if'/dashboard/user/' in pathname:
            return personalised_dashboard.layout

if __name__ == '__main__':
    app.run_server(port=80)