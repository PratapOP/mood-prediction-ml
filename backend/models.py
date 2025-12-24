from .extention import db
from flask_login import UserMixin
from datetime import datetime
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

class MoodEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    mood_result = db.Column(db.Integer)

    sleep_hours = db.Column(db.Float)
    screen_time = db.Column(db.Float)
    physical_activity = db.Column(db.Float)
    work_hours = db.Column(db.Float)
    social_interaction = db.Column(db.Float)
    caffeine_intake = db.Column(db.Integer)
