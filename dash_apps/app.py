import dash
import os
from flask import Flask

server = Flask(__name__)
app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True
server=app.server
server.secret_key = os.environ.get('secret_key', 'secret')