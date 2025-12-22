import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
import joblib  # This is used to save the model to a file

# 1. LOAD DATA
df = pd.read_csv('data/mood_data.csv')

# 2. SEPARATE FEATURES AND TARGET
# X = the factors (sleep, screen time, etc.)
# y = the result we want to predict (mood)
X = df.drop('mood', axis=1) 
y = df['mood']

# 3. SPLIT FOR TESTING
# We keep 20% of data secret to test the model later
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. INITIALIZE THE MODEL
# 'max_depth=3' keeps the tree simple and prevents it from "memorizing" noise
model = DecisionTreeClassifier(max_depth=3, random_state=42)

# 5. TRAIN (The "Learning" Step)
model.fit(X_train, y_train)

# 6. SAVE THE BRAIN
# We save the model as a .joblib file so the Frontend can use it later
joblib.dump(model, 'model/mood_model.joblib')

print("Success: Model trained and saved to model/mood_model.joblib")