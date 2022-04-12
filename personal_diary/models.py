from app import db


class Entry(db.Model):
    """Data model for diary entries"""

    __tablename__ = 'diary-entries'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), unique=False, nullable=False)
    body = db.Column(db.Text, unique=False, nullable=False)
    created = db.Column(db.DateTime, unique=False, nullable=False)
    modified = db.Column(db.DateTime, unique=False, nullable=True)
    folder = db.Column(db.String(), unique=False, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return '<Entry {}>'.format(self.id)


class User(db.Model):
    """Data model for users"""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    entries = db.relationship('Entry', backref='user', lazy=True)

    def __repr__(self):
        return '<User {}>'.format(self.id)
