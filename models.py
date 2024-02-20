from flask_sqlalchemy import SQLAlchemy
from flask import jsonify

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class AccessToken(db.Model):
    __bind_key__ = 'tokens'
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(32), unique=True, nullable=False)
    username = db.Column(db.String(32), unique=True, nullable=False)
    expiry_time = db.Column(db.DateTime, nullable=False)

class Notes(db.Model):
    __bind_key__ = 'notes'
    id = db.Column(db.Integer, primary_key=True)
    created_by = db.Column(db.String(100), nullable=False)
    created_on = db.Column(db.DateTime, nullable=False)
    modified_by = db.Column(db.String(100), nullable=False)
    modified_on = db.Column(db.DateTime, nullable=False)
    message = db.Column(db.String(1000), nullable=False)
    access_list = db.Column(db.String(255), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'created_by': self.created_by,
            'created_on': self.created_on.strftime('%Y-%m-%d %H:%M:%S'),
            'modified_by': self.modified_by,
            'modified_on': self.modified_on.strftime('%Y-%m-%d %H:%M:%S'),
            'message': self.message,
            'access_list': self.access_list.split(',') if self.access_list else []
        }