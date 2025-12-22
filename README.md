# 🎯 Mood Prediction from Daily Routine

An end-to-end Machine Learning application that predicts a user's daily mood based on lifestyle habits (sleep, exercise, work, etc.) using a **Decision Tree Classifier**. This project bridges the gap between a raw data science model and a functional user interface.

## 🌟 Features

* **Data-Driven Predictions**: Uses a Decision Tree model to classify mood into four categories: Happy, Neutral, Stressed, and Sad.
* **Interactive UI**: A clean, responsive frontend for data entry.
* **Mood Timeline**: Visualizes mood trends over time using **Chart.js**.
* **REST API**: A Flask-based backend that handles communication between the ML model and the browser.

## 🛠️ Tech Stack

* **Frontend**: HTML5, CSS3, JavaScript (ES6), Chart.js
* **Backend**: Python 3.x, Flask, Flask-CORS
* **Machine Learning**: Scikit-Learn, Pandas, NumPy
* **Model Persistence**: Joblib

## 📊 The Machine Learning Model

The core of this project is a **DecisionTreeClassifier**.

* **The Data**: 200 simulated entries mapping routine habits to emotional states.
* **The Logic**: The model uses **Gini Impurity** to determine the most significant factors affecting mood. In this dataset, `sleep_hours` and `work_hours` were identified as the primary indicators of emotional well-being.
* **Explainability**: Unlike "black-box" models, the Decision Tree allows us to see the exact logic gates used to reach a prediction.

## 📂 Project Structure

```text
mood-prediction/
│── data/           # Contains mood_data.csv
│── model/          # Contains the serialized mood_model.joblib
│── app/            # Backend (Flask API, Training & Prediction scripts)
│── frontend/       # UI (HTML, CSS, JS)
│── requirements.txt# Python dependencies
└── README.md       # Project documentation

```

## 🚀 Installation & Setup

### 1. Clone and Environment

```bash
git clone https://github.com/PratapOP/mood-prediction-ml.git
cd mood-prediction-ml
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

```

### 2. Install Dependencies

```bash
pip install -r requirements.txt

```

### 3. Initialize the Model

Run the training script to generate the dataset and save the trained model:

```bash
python app/train_model.py

```

### 4. Run the Application

Start the Flask server:

```bash
python app/main.py

```

Then, simply open `frontend/index.html` in your favorite web browser.

## 📈 Future Improvements

* [ ] Add **SQLite** database support to save mood history permanently.
* [ ] Implement **Random Forest** for higher accuracy.
* [ ] Add user authentication for personalized tracking.

---

### 💡 What I Learned

Through this project, I mastered the process of:

1. Simulating a dataset with realistic correlations.
2. Handling **Pathing** and **CORS** issues in a full-stack environment.
3. Serializing ML models for production use.
4. Visualizing real-time model inferences on a frontend dashboard.
