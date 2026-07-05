import os

migration_directory = "migrations"
SQLALCHEMY_TRACK_MODIFICATIONS = False
# keep plain 404 messages instead of flask-restx's "did you mean" suggestions
ERROR_404_HELP = False
SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg://ods:' + os.environ['POSTGRES_PASSWORD'] + '@db/open-dccon-selector'
