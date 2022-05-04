from personal_diary import db
from flask_login import UserMixin

"""
Association table for entries and tags, as describe by Flask-SQLAlchemy documentation
"""
tags = db.Table('tags',
                db.Column('tag_id', db.Integer, db.ForeignKey('EntryTags.id'), primary_key=True),
                db.Column('entry_id', db.String, db.ForeignKey('DiaryEntries.id'), primary_key=True)
                )


class Tag(db.Model):
    """Data model for diary entry tags"""

    __tablename__ = 'EntryTags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)


class Entry(UserMixin, db.Model):
    """Data model for diary entries"""

    __tablename__ = 'DiaryEntries'

    id = db.Column(db.String(), primary_key=True)
    title = db.Column(db.String(), unique=False, nullable=False)
    body = db.Column(db.Text, unique=False, nullable=False)
    created = db.Column(db.DateTime, unique=False, nullable=False)
    modified = db.Column(db.DateTime, unique=False, nullable=True)
    tags = db.relationship('Tag', secondary=tags, lazy='subquery', backref=db.backref('entries', lazy=True))
    user_id = db.Column(db.String(), db.ForeignKey('Users.id'), nullable=False)
    mood = db.Column(db.Text, unique=False, nullable=False)


class User(UserMixin, db.Model):
    """Data model for users"""

    __tablename__ = 'Users'

    id = db.Column(db.String(), primary_key=True)
    username = db.Column(db.String(15), unique=True)
    name = db.Column(db.String(30))
    password = db.Column(db.String(15))
    entries = db.relationship('Entry', backref='Users', lazy=True, cascade="all, delete-orphan")
