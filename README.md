# 🎯 Mood Prediction from Daily Routine

A full-stack Machine Learning application that predicts daily mood based on routine habits using a **Decision Tree Classifier**.

## 🚀 Features
- **ML Engine**: Scikit-Learn Decision Tree (Gini Impurity).
- **Backend**: Flask API for real-time inference.
- **Frontend**: Interactive UI with **Chart.js** mood tracking.

## 🛠️ Setup Instructions
1. Clone the repo.
2. Create venv: `python -m venv venv`
3. Install deps: `pip install -r requirements.txt`
4. Train model: `python app/train_model.py`
5. Start server: `python app/main.py`
6. Open `frontend/index.html` in your browser.

## 📊 Data Insights
The model prioritizes **Sleep Hours** and **Work Hours** as the primary split nodes for determining emotional states.