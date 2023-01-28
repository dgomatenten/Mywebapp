import sqlite3

import click
from flask import current_app
from flask_sqlalchemy import SQLAlchemy



#g is a special object that is unique for each request. It is used to store data that might be accessed by multiple functions during the request. 
# The connection is stored and reused instead of creating a new connection if get_db is called a second time in the same request.

from flask import g


def get_db():
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    
    if "db" not in g:
        #sqlite3.connect() establishes a connection to the file pointed at by the DATABASE configuration key. 
        # This file doesn’t have to exist yet, and won’t until you initialize the database later.

        g.db = sqlite3.connect(
            #current_app is another special object that points to the Flask application handling the request. 
            # Since you used an application factory, there is no application object when writing the rest of your code. 
            # get_db will be called when the application has been created and is handling a request, so current_app can be used.
   
            current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )

        #sqlite3.Row tells the connection to return rows that behave like dicts. This allows accessing the columns by name.
        g.db.row_factory = sqlite3.Row

    return g.db

def get_flightdb():
    db = sqlite3.connect(
            current_app.config["FLIGHTDB"], detect_types=sqlite3.PARSE_DECLTYPES
        )
    db.row_factory = sqlite3.Row

    return db

def get_worddb(app):
    worddb = SQLAlchemy(app)
    return worddb

def close_db(e=None):
    """If this request connected to the database, close the
    connection.
    """
    db = g.pop("db", None)

    if db is not None:
        db.close()




def init_db():
    """Clear existing data and create new tables."""
    db = get_db()

    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))

#click.command() defines a command line command called init-db that calls the init_db function and shows a success message to the user. 
# You can read Command Line Interface to learn more about writing commands.

@click.command("init-db")
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")


def init_app(app):
    """Register database functions with the Flask app. This is called by
    the application factory.
    """
    #app.teardown_appcontext() tells Flask to call that function when cleaning up after returning the response.
    #app.cli.add_command() adds a new command that can be called with the flask command.
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
