from flask import Flask, render_template, redirect, url_for
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from twitch import TwitchClient

from . import config as config
from .consts import TWITCH_EXTENSION_CLIENT_ID

app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)
api = Api(app)
migrate = Migrate(app, db)
cors = CORS(app)

twitchClient = TwitchClient(client_id=TWITCH_EXTENSION_CLIENT_ID)

from . import models
from . import apis

@app.route('/')
def index():
    return redirect(url_for('overlay'))

@app.route('/config')
def config():
    return render_template('config.html')

@app.route('/overlay')
def overlay():
    return render_template('viewer.html')

@app.route('/live-config')
def live_config():
    return render_template('live-config.html')
