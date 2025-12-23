from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import joblib
import pandas as pd
import os
from datetime import datetime
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
# CORS must be configured to allow credentials (cookies) for authentication
CORS(app, supports_credentials=True)
app.config['SECRET_KEY'] = 'your-very-secret-key-here' # Required for flask-login

# 1. Database Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'mood_history.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 2. Login Manager Configuration
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 3. Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    # Relationship: One user has many mood entries
    entries = db.relationship('MoodEntry', backref='owner', lazy=True)

class MoodEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.String(20), default=lambda: datetime.now().strftime("%Y-%m-%d %H:%M"))
    sleep = db.Column(db.Float)
    work = db.Column(db.Float)
    exercise = db.Column(db.Float)
    mood_result = db.Column(db.String(20))

# Create the database tables
with app.app_context():
    db.create_all()

# Load Model
MODEL_PATH = os.path.join(BASE_DIR, '../model/mood_model.joblib')
model = joblib.load(MODEL_PATH)

# --- AUTH ROUTES ---

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400
    
    hashed_pw = generate_password_hash(data['password'])
    new_user = User(username=data['username'], password_hash=hashed_pw)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully!'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user and check_password_hash(user.password_hash, data['password']):
        login_user(user)
        return jsonify({'message': 'Logged in!', 'username': user.username})
    return jsonify({'error': 'Invalid username or password'}), 401

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out!'})

# --- APP ROUTES ---

@app.route('/predict', methods=['POST'])
@login_required # Only logged in users can predict and save
def predict():
    data = request.json
    
    # 1. ML Prediction Logic
    input_df = pd.DataFrame([{
        'sleep_hours': float(data['sleep']),
        'screen_time': float(data['screen']),
        'physical_activity': float(data['exercise']),
        'work_hours': float(data['work']),
        'social_interaction': float(data['social']),
        'caffeine_intake': float(data['caffeine'])
    }])
    prediction = model.predict(input_df)[0]

    # 2. Save to Database for specific user
    new_entry = MoodEntry(
        user_id=current_user.id,
        sleep=float(data['sleep']),
        work=float(data['work']),
        exercise=float(data['exercise']),
        mood_result=prediction
    )
    db.session.add(new_entry)
    db.session.commit()

    # 3. Feature importance
    importances = model.feature_importances_.tolist()
    feature_names = ['Sleep', 'Screen Time', 'Exercise', 'Work', 'Social', 'Caffeine']
    importance_map = dict(zip(feature_names, importances))

    return jsonify({
        'mood': prediction,
        'importance': importance_map
    })

@app.route('/history', methods=['GET'])
@login_required # Only see YOUR history
def get_history():
    entries = MoodEntry.query.filter_by(user_id=current_user.id).order_by(MoodEntry.id.desc()).limit(10).all()
    history = [{'date': e.date, 'mood': e.mood_result} for e in entries]
    return jsonify(history[::-1])

# --- THE IGNITION SWITCH ---
if __name__ == '__main__':
    print("Starting Flask server on http://127.0.0.1:5000")
    app.run(port=5000, debug=True)