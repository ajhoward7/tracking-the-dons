import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from plotly_plotting import preprocess_activities
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from datetime import *

from apps import alex_dashboard
from apps import personalised_dashboard_2
from app import app

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/preloaded/alex':
        return alex_dashboard.layout
    elif '/dashboard/user/' in pathname:
        return personalised_dashboard_2.layout  # CHANGE
    else:
        return 'No page here :-('

if __name__ == '__main__':
    app.run_server(port=8050, debug=True)