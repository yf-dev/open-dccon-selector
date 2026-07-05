# noinspection PyUnresolvedReferences
from app import app, db


@app.cli.command('drop_all')
def drop_all():
    db.drop_all()
