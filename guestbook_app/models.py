# guestbook_app/models.py

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Pesan(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  pesan = db.Column(db.Text, nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

  def __repr__(self):
      return f'<Pesan {self.id}>'

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), unique=True, nullable=False)
  password = db.Column(db.String(120), nullable=False)
  pesan = db.relationship('Pesan', backref='user', lazy=True)

  def __repr__(self):
    return f'<User {self.username}>'