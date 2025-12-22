import joblib
import pandas as pd
import os

# 1. Setup paths (using the 'root' perspective that worked for you)
MODEL_PATH = 'model/mood_model.joblib'

def predict_daily_mood(sleep, screen, exercise, work, social, caffeine):
    # Load the saved model
    if not os.path.exists(MODEL_PATH):
        return "Error: Model file not found. Please run train_model.py first."
    
    model = joblib.load(MODEL_PATH)
    
    # 2. Prepare the input data
    # The model expects a DataFrame with the exact same column names as training
    input_data = pd.DataFrame([[sleep, screen, exercise, work, social, caffeine]], 
                              columns=['sleep_hours', 'screen_time', 'physical_activity', 
                                       'work_hours', 'social_interaction', 'caffeine_intake'])
    
    # 3. Make the prediction
    prediction = model.predict(input_data)
    
    return prediction[0]

# 4. A quick test block to run from the terminal
if __name__ == "__main__":
    print("--- Mood Predictor Test ---")
    # Test case: High sleep, high exercise, low work
    result = predict_daily_mood(8.5, 2.0, 45, 4.0, 8, 1)
    print(f"Predicted Mood: {result}")