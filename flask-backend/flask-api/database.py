from flask import current_app, g
from flask.cli import with_appcontext
import click
import sqlite3


def init_app(app):
    """
    registers function with the flask app factory
    """
    # disconnect from db on exit:
    app.teardown_appcontext(close_db)
    # add click cli command to flask command:
    app.cli.add_command(init_db_cli)


def init_db():
    """
    applies the schema to (re)create the database
    """
    db = get_db()

    with current_app.open_resource("schema.sql") as schema:
        db.executescript(schema.read().decode("utf8"))


@click.command("init-db")
@with_appcontext
def init_db_cli():
    """
    recreate database tables (all data is lost)
    """
    # called via: flask init-db

    init_db()
    click.echo("database initialized")


def get_db():
    """
    creates database connection or gets existing one from app context

    returns db attribute
    """
    # check for 'db' attribute in current app context:
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"],
            detect_types=sqlite3.PARSE_DECLTYPES,
        )
        g.db.row_factory = sqlite3.Row  # rows can be accessed like dicts.

    return g.db


def close_db(e=None):
    """
    closes database connection (if one exists)
    """
    db = g.pop("db", None)

    if db is not None:
        db.close()
