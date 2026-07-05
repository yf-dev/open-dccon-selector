from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy

from . import config as config

app = Flask(__name__, static_folder='/frontend/dist/static', template_folder='/frontend/dist')
app.config.from_object(config)
db = SQLAlchemy(app)
# no swagger doc/specs endpoints; add_specs is only honored via init_app()
api = Api(doc=False)
api.init_app(app, add_specs=False)
migrate = Migrate(app, db)
cors = CORS(app)

from . import models
from . import apis
