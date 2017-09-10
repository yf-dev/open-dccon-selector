# noinspection PyUnresolvedReferences
from app import app, db
from flask_script import Manager
from flask_migrate import MigrateCommand

manager = Manager(app)
manager.add_command('db', MigrateCommand)

@manager.command
def drop_all():
    db.drop_all()


if __name__ == '__main__':
    manager.run()
