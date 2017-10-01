from flask import Flask, render_template, redirect
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from . import config as config

app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)
api = Api(app)
migrate = Migrate(app, db)
cors = CORS(app)

from . import models
from . import apis


@app.route('/config')
def index():
    return render_template("config.html")

@app.route('/overlay')
@app.route('/')
def index():
    return render_template("overlay.html")

@app.route('/live-config')
def index():
    return render_template("live-config.html")
