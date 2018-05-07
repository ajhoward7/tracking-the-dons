import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from plotly_plotting import preprocess_activities
from datetime import *
import polyline

from app import app

app.layout = html.Div("<a href='www.google.com'> Here is some HTML</a>")
