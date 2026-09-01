"""
train_model.py

This script trains a simple AI model that predicts health status
("Normal" or "Needs Attention") based on:
  - body temperature
  - how the person is feeling (good / tired / sick)
  - how many medicine doses they missed

Run this file ONCE to create the model file (health_model.pkl).
The main app then loads that saved model instead of retraining every time.
"""

import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
import joblib

# ---------- Step 1: Create sample training data ----------
# In a real project this would come from real patient records.
# Here we create realistic sample data by hand so the model has
# something to learn from.

data = {
    "temperature": [98.6, 99.0, 101.2, 100.8, 98.4, 102.0, 99.5, 98.0,
                     100.5, 97.9, 101.5, 98.7, 99.2, 103.0, 98.1, 100.9],
    "feeling":     ["good", "good", "sick", "tired", "good", "sick", "tired", "good",
                     "sick", "good", "sick", "good", "tired", "sick", "good", "tired"],
    "missed_doses": [0, 0, 2, 1, 0, 3, 1, 0,
                      2, 0, 3, 0, 1, 3, 0, 1],
    "health_status": ["Normal", "Normal", "Needs Attention", "Needs Attention", "Normal",
                       "Needs Attention", "Needs Attention", "Normal", "Needs Attention",
                       "Normal", "Needs Attention", "Normal", "Needs Attention",
                       "Needs Attention", "Normal", "Needs Attention"],
}

df = pd.DataFrame(data)

# ---------- Step 2: Convert text columns into numbers ----------
# Machine learning models only understand numbers, so we convert
# "feeling" (good/tired/sick) into numeric codes.

feeling_encoder = LabelEncoder()
df["feeling_encoded"] = feeling_encoder.fit_transform(df["feeling"])

X = df[["temperature", "feeling_encoded", "missed_doses"]]
y = df["health_status"]

# ---------- Step 3: Train the model ----------

model = DecisionTreeClassifier(max_depth=3, random_state=42)
model.fit(X, y)

# ---------- Step 4: Save the trained model and the encoder ----------
# We save both so the app can use the exact same encoding later.

joblib.dump(model, "health_model.pkl")
joblib.dump(feeling_encoder, "feeling_encoder.pkl")

print("Model trained and saved successfully!")
print("Files created: health_model.pkl, feeling_encoder.pkl")
