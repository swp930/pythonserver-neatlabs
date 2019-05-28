from app import db
from pytz import timezone

class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    author = db.Column(db.String())
    published = db.Column(db.String())

    def __init__(self, name, author, published):
        self.name = name
        self.author = author
        self.published = published

    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    def serialize(self):
        return {
            'id': self.id, 
            'name': self.name,
            'author': self.author,
            'published':self.published
        }

class MoodData(db.Model):
    __tablename__ = 'mooddata'

    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String())
    datapoints = db.Column(db.String())
    date = db.Column(db.DateTime())
    uniqueidentifier = db.Column(db.String())

    def __init__(self, data, datapoints, date, uniqueidentifier):
        self.data = data
        self.datapoints = datapoints
        self.date = date
        self.uniqueidentifier = uniqueidentifier

    def __repr__(self):
    	return '<id {}>'.format(self.id)

    def serialize(self):
        self.date = self.date.astimezone(timezone('US/Pacific'))
        return {
            'id': self.id,
			'data': self.data,
            'datapoints': self.datapoints,
            'date': self.date,
            'uniqueidentifier': self.uniqueidentifier
    	}

class UserData(db.Model):
    __tablename__ = 'userdata'

    id = db.Column(db.Integer, primary_key=True)
    uniqueidentifier = db.Column(db.String())
    waketime = db.Column(db.String())
    sleeptime = db.Column(db.String())

    def __init__(self, uniqueidentifier, waketime, sleeptime):
        self.uniqueidentifier = uniqueidentifier
        self.waketime = waketime
        self.sleeptime = sleeptime
    
    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'uniqueidentifier': self.uniqueidentifier,
            'waketime': self.waketime,
            'sleeptime': self.sleeptime,
            'email': 'not set'
        }