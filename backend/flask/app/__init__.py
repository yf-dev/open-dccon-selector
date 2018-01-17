from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from twitch import TwitchClient

from . import config as config
from .consts import TWITCH_EXTENSION_CLIENT_ID

app = Flask(__name__, static_folder='/frontend/dist/static', template_folder='/frontend/dist')
app.config.from_object(config)
db = SQLAlchemy(app)
api = Api(app)
migrate = Migrate(app, db)
cors = CORS(app)

twitchClient = TwitchClient(client_id=TWITCH_EXTENSION_CLIENT_ID)

from . import models
from . import apis
