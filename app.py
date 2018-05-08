import dash
import os
from flask import Flask

server = Flask(__name__)
app = dash.Dash(__name__, url_base_pathname='/dashboard/')
app.config.suppress_callback_exceptions = True
server=app.server