import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from plotly_plotting import preprocess_activities
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from datetime import *

from apps import alex_dashboard
from apps import personalised_dashboard
from app import app

app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/preloaded/alex':
         return alex_dashboard.layout
    elif pathname == '/dynamic':
        return alex_dashboard.layout  # CHANGE
    else:
        return 'Uh-oh'

if __name__ == '__main__':
    app.run_server(port=998, debug=True)