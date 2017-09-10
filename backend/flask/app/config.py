import os

migration_directory = "migrations"
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://ods:' + os.environ['POSTGRES_PASSWORD'] + '@db/open-dccon-selector'
debug = True
