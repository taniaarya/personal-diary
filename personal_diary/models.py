from personal_diary import db
from flask_login import UserMixin


class Entry(UserMixin, db.Model):
    """Data model for diary entries"""

    __tablename__ = 'DiaryEntries'

    id = db.Column(db.String(), primary_key=True)
    title = db.Column(db.String(), unique=False, nullable=False)
    body = db.Column(db.Text, unique=False, nullable=False)
    created = db.Column(db.DateTime, unique=False, nullable=False)
    modified = db.Column(db.DateTime, unique=False, nullable=True)
    folder = db.Column(db.String(), unique=False, nullable=True)
    user_id = db.Column(db.String(), db.ForeignKey('Users.id'), nullable=False)

    def __repr__(self):
        return '<Entry {}>'.format(self.id)


class User(UserMixin, db.Model):
    """Data model for users"""

    __tablename__ = 'Users'

    id = db.Column(db.String(), primary_key=True)
    username = db.Column(db.String(15), unique=True)
    name = db.Column(db.String(30))
    password = db.Column(db.String(15))
    entries = db.relationship('Entry', backref='Users', lazy=True)

    def __repr__(self):
        return '<User {}>'.format(self.id)
