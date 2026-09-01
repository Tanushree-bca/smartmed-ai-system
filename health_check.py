import streamlit as st
import joblib
import os
from storage import save_record

MODEL_FILE = "health_model.pkl"
ENCODER_FILE = "feeling_encoder.pkl"


def load_ai_model():
    if os.path.exists(MODEL_FILE) and os.path.exists(ENCODER_FILE):
        model = joblib.load(MODEL_FILE)
        encoder = joblib.load(ENCODER_FILE)
        return model, encoder
    return None, None


def predict_health_status(model, encoder, temperature, feeling, missed_doses):
    feeling_encoded = encoder.transform([feeling])[0]
    features = [[temperature, feeling_encoded, missed_doses]]
    prediction = model.predict(features)[0]
    return prediction


def show():
    st.subheader("🩺 Health Check (AI Powered)")
    st.write("Enter your details below and let the trained AI model assess your health status.")

    model, encoder = load_ai_model()

    if model is None:
        st.error(
            "⚠️ AI model not found. Please run 'python train_model.py' once "
            "in this folder to create the model files."
        )
        return

    col1, col2, col3 = st.columns(3)
    with col1:
        temperature = st.number_input("🌡️ Temperature (°F)", min_value=90.0, max_value=110.0, value=98.6, step=0.1)
    with col2:
        feeling = st.selectbox("😊 Feeling", ["good", "tired", "sick"])
    with col3:
        missed_doses = st.slider("💊 Missed doses today", 0, 5, 0)

    if st.button("🔍 Check Health Status"):
        health_status = predict_health_status(model, encoder, temperature, feeling, missed_doses)

        st.markdown("---")
        if health_status == "Needs Attention":
            st.error(f"### 🚨 AI Prediction: {health_status}")
            st.write("Please monitor your symptoms and consider resting or consulting a doctor.")
        else:
            st.success(f"### ✅ AI Prediction: {health_status}")
            st.write("Your health status looks normal today. Keep it up!")

        record = {
            "type": "health_check",
            "temperature": temperature,
            "feeling": feeling,
            "missed_doses": missed_doses,
            "health_status": health_status,
        }
        save_record(record)
        st.toast("Data saved successfully ✅")
