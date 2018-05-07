from flask import Flask, redirect, render_template, url_for, flash, request

from scrape import scrape_activities
from credentials import client_id, client_secret
import requests
import json


redirect_url = 'https://www.strava.com/oauth/authorize?response_type=code&redirect_uri=http%3A%2F%2F54.214.153.34%2Fauthorize&client_id=20812'


server = Flask(__name__)

@server.route('/')
def home():
    return render_template('index.html', strava_url=redirect_url, preloaded_url='http://127.0.0.1:8050/preloaded/alex')


@server.route('/authorize', methods=('GET','POST'))
def authorize():
    code = request.args.get('code')
    r = requests.post('https://www.strava.com/oauth/token', data={'client_id':client_id, 'client_secret':client_secret, 'code':code})
    json_data = json.loads(r._content)
    access_token = json_data["access_token"]
    username = scrape_activities(access_token)

    ip = '127.0.0.1:5000'

    return redirect('http://{}/{}'.format(ip,username))


if __name__ == "__main__":
    server.run(debug=True)
