# AI-Based Student Performance Prediction & Academic Analytics

## Problem Statement
Predicts student academic risk and provides actionable insights to improve outcomes,
using demographic and contextual factors (parental education, economic indicator via
lunch type, test preparation access).

## How it works
1. **EDA** (`notebooks/eda.py`) — explored 1000 student records, found key performance drivers:
   test prep completion, lunch type (economic proxy), parental education level.
2. **Model** (`notebooks/train_risk_model.py`) — Random Forest Classifier flags students
   as "at-risk" (predicted avg score < 60) with a probability score, 61% accuracy on held-out data.
3. **App** (`app/app.py`) — Streamlit interface: enter a student's profile, get a risk %
   and specific, actionable intervention suggestions.

## Run locally
```
cd app
pip install streamlit pandas scikit-learn joblib
streamlit run app.py
```

## Scalability
Designed to plug into live school data (attendance systems, LMS activity, past test
scores) for continuous, automated, school-wide risk monitoring — not just a one-off prediction.

## Tech stack
Python, Pandas, Scikit-learn (Random Forest), Streamlit
