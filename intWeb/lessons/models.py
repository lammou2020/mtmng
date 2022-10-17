# Copyright 2015 Google Inc.
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

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
'''
class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(255), unique=True)
    Pass = db.Column(db.String(255))
    Name = db.Column(db.String(255))
    Classno = db.Column(db.String(255))
    Seat = db.Column(db.String(255))
    Role = db.Column(db.String(255))
    def __init__(self, user=None, Pass=None,Name=None,Role=None,Classno=None,Seat=None):
        self.user = user
        self.Pass = Pass
        self.Name = Name
        self.Role=Role
        self.Classno=Classno
        self.Seat=Seat
    def __repr__(self):
        return "<User(User='%s', Role=%s)" % (self.user, self.Role)

def readUser(UserName):
    result = User.query.filter_by(user=UserName).first()
    #get(UserName)
    if not result:
        return None
    return from_sql(result)
'''
#insert into user (user,Pass,Name,Role) values('admin','123','admin',1);

class Lesson(db.Model):
    __tablename__ = 'Lesson'
    id = db.Column(db.Integer, primary_key=True)
    Lesson = db.Column(db.String(255), unique=True)
    Title = db.Column(db.String(255))
    Path = db.Column(db.String(255), unique=True)
    Descr = db.Column(db.Text)
    logDate = db.Column(db.String(255))
    Classno = db.Column(db.String(255))
    Open = db.Column(db.Integer)
    imageUrl = db.Column(db.String(255))
    createdById = db.Column(db.String(255))
    def __init__(self, Lesson=None, Title=None,Path=None,Classno=None,Open=None,createdById=None,Descr=None,logDate=None,imageUrl=None):
        self.Lesson= Lesson
        self.Title =Title 
        self.Path = Path 
        self.Descr =Descr 
        self.logDate=logDate
        self.Classno=Classno
        self.Open = Open 
        self.imageUrl=imageUrl
        self.createdById=createdById
    def __repr__(self):
        return "<Lesson(Lesson='%s', Title=%s)" % (self.Lesson, self.Title)

def list(limit=10, cursor=None):
    cursor = int(cursor) if cursor else 0
    query = (Lesson.query
             .filter_by(Open=1)
             .order_by(Lesson.id)
             .limit(limit)
             .offset(cursor))
    lessons = builtin_list(map(from_sql, query.all()))
    next_page = cursor + limit if len(lessons) == limit else None
    return (lessons, next_page)

# [START list_by_user]
def list_by_user(user_id, limit=10, cursor=None):
    cursor = int(cursor) if cursor else 0
    query = (Lesson.query
             .filter_by(createdById=user_id)
             .order_by(Lesson.Title)
             .limit(limit)
             .offset(cursor))
    lessons = builtin_list(map(from_sql, query.all()))
    next_page = cursor + limit if len(lessons) == limit else None
    return (lessons, next_page)
# [END list_by_user]

def read(id):
    result = Lesson.query.get(id)
    if not result:
        return None
    return from_sql(result)

def create(data):
    lesson = Lesson(**data)
    db.session.add(lesson)
    db.session.commit()
    return from_sql(lesson)

def update(data, id):
    lesson = Lesson.query.get(id)
    for k, v in data.items():
        setattr(lesson, k, v)
    db.session.commit()
    return from_sql(lesson)

def delete(id):
    Lesson.query.filter_by(id=id).delete()
    db.session.commit()

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
