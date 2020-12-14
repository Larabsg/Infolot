from flask import Flask
import click
import os

from flask.cli import with_appcontext

from flask_sqlalchemy import SQLAlchemy

from flask_bcrypt import Bcrypt

#sqlite:///rede_social.db

db = SQLAlchemy()

bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('config')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'rede_social.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)

    bcrypt.init_app(app)

    app.cli.add_command(init_db_command)
    with app.app_context():
        from . import routes
    return app

@click.command('init-db')
@with_appcontext
def init_db_command():
    from . import entidades
    db.create_all()
    click.echo('Criei o banco com sucesso.')

app = create_app()