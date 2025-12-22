from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import os

app = Flask(__name__)
CORS(app) # This allows your HTML file to talk to this Python server

# Load the model once when the server starts
MODEL_PATH = os.path.join(os.path.dirname(__file__), '../model/mood_model.joblib')
model = joblib.load(MODEL_PATH)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    
    # Convert incoming JSON to DataFrame for the model
    input_df = pd.DataFrame([{
        'sleep_hours': float(data['sleep']),
        'screen_time': float(data['screen']),
        'physical_activity': float(data['exercise']),
        'work_hours': float(data['work']),
        'social_interaction': float(data['social']),
        'caffeine_intake': float(data['caffeine'])
    }])
    
    prediction = model.predict(input_df)[0]
    return jsonify({'mood': prediction})

if __name__ == '__main__':
    app.run(port=5000, debug=True)