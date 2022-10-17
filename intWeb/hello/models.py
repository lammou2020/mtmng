# Copyright 2015 Google Inc.
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime
builtin_list = list

from intWeb import db
#db = SQLAlchemy()

def init_app(app):
    # Disable track modifications, as it unnecessarily uses memory.
    app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', False)
    db.init_app(app)

def from_sql(row):
    """Translates a SQLAlchemy model instance into a dictionary"""
    data = row.__dict__.copy()
    data['id'] = row.id
    data.pop('_sa_instance_state')
    return data

class Todo(db.Model):
    __tablename__ = "todos"
    id = db.Column("todo_id", db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    text = db.Column(db.String(225))
    done = db.Column(db.Boolean)
    pub_date = db.Column(db.DateTime)

    def __init__(self, title, text):
        self.title = title
        self.text = text
        self.done = False
        self.pub_date = datetime.datetime.now(datetime.timezone.utc)
        #datetime.utcnow()


def _create_database():
    """
    If this script is run directly, create all the tables necessary to run the application.
    """
    app = Flask(__name__)
    app.config.from_pyfile('../../config.py')
    init_app(app)
    with app.app_context():
        db.drop_all()
        db.create_all()
        db.session.commit()
    print("All tables created")

if __name__ == '__main__':
    _create_database()
