# coding:utf-8

from flask import session
from ihome import create_app, db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

# create flask object
app = create_app("develop")
manager = Manager(app)
Migrate(app, db)
manager.add_command("db", MigrateCommand)

if __name__ == '__main__':
    manager.run()


# python manager.py db migrate
# python manager.py db update

