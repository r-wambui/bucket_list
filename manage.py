from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager, prompt_bool
from flask_migrate import Migrate, MigrateCommand

from models import db


app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')


db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)


@manager.command
def dropdb():
    if prompt_bool("Are you sure you want to drop the database"):
        db.drop_all()

@manager.command
def createdb(default_data=True, sample_data=False):
        db.create_all()


manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
