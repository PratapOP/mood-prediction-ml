from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import joblib, pandas as pd, os
from datetime import datetime

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config['SECRET_KEY'] = 'super-secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mood_history.db'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password_hash = db.Column(db.String(120))

class MoodEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date = db.Column(db.String(50), default=lambda: datetime.now().strftime("%H:%M"))
    mood_result = db.Column(db.String(50))

@login_manager.user_loader
def load_user(uid): return db.session.get(User, int(uid))

with app.app_context(): db.create_all()

model = joblib.load('model/mood_model.joblib')

@app.route('/register', methods=['POST'])
def reg():
    data = request.json
    if User.query.filter_by(username=data['username']).first(): return jsonify({'error': 'Exists'}), 400
    user = User(username=data['username'], password_hash=generate_password_hash(data['password']))
    db.session.add(user); db.session.commit()
    return jsonify({'message': 'Ok'})

@app.route('/login', methods=['POST'])
def log():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user and check_password_hash(user.password_hash, data['password']):
        login_user(user); return jsonify({'message': 'Ok'})
    return jsonify({'error': 'Wrong'}), 401

@app.route('/predict', methods=['POST'])
@login_required
def predict():
    data = request.json
    try:
        # We take 'sleep' from JS and map it to 'sleep_hours' for the model
        input_df = pd.DataFrame([{
            'sleep_hours': float(data['sleep']),
            'screen_time': float(data['screen']),
            'physical_activity': float(data['exercise']),
            'work_hours': float(data['work']),
            'social_interaction': float(data['social']),
            'caffeine_intake': float(data['caffeine'])
        }])
        
        prediction = model.predict(input_df)[0]
        
        # Calculate feature importance so the JS chart doesn't break
        importances = model.feature_importances_
        importance_map = dict(zip(['Sleep', 'Screen', 'Exercise', 'Work', 'Social', 'Caffeine'], importances.tolist()))

        new_entry = MoodEntry(
            user_id=current_user.id,
            mood_result=prediction
        )
        db.session.add(new_entry)
        db.session.commit()

        return jsonify({
            'mood': prediction,
            'importance': importance_map
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/history', methods=['GET'])
@login_required
def history():
    entries = MoodEntry.query.filter_by(user_id=current_user.id).all()
    return jsonify([{'date': e.date, 'mood': e.mood_result} for e in entries])

if __name__ == '__main__':
    app.run(debug=True)