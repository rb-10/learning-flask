import sqlite3

import click
from flask import current_app, g

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()
    try:
        with current_app.open_resource('schema.sql') as f:
            db.executescript(f.read().decode('utf8'))
    
    except sqlite3.DatabaseError as e:
        print(f"An error occurred: {e}")

@click.command('init-db')
def init_db_command():
    """Drop if exists and create the databases"""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)