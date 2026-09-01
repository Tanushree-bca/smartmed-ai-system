import streamlit as st
import joblib
import os
from storage import save_record

MODEL_FILE = "health_model.pkl"
ENCODER_FILE = "feeling_encoder.pkl"


def load_ai_model():   
    """Load the trained AI model and the feeling encoder from disk."""
    if os.path.exists(MODEL_FILE) and os.path.exists(ENCODER_FILE):
        model = joblib.load(MODEL_FILE)
        encoder = joblib.load(ENCODER_FILE)
        return model, encoder
    return None, None


def predict_health_status(model, encoder, temperature, feeling, missed_doses):
    """Use the trained AI model to predict health status."""
    feeling_encoded = encoder.transform([feeling])[0]
    features = [[temperature, feeling_encoded, missed_doses]]
    prediction = model.predict(features)[0]
    return prediction


def show():
    st.header("Health Check (AI Powered)")

    model, encoder = load_ai_model()

    if model is None:
        st.error(
            "AI model not found. Please run 'python train_model.py' once "
            "in this folder to create the model files."
        )
        return

    temperature = st.number_input(
        "Body temperature (°F)", min_value=90.0, max_value=110.0, value=98.6, step=0.1
    )
    feeling = st.selectbox("How are you feeling today?", ["good", "tired", "sick"])
    missed_doses = st.slider("How many medicine doses did you miss today?", 0, 5, 0)

    if st.button("Check Health Status"):
        health_status = predict_health_status(model, encoder, temperature, feeling, missed_doses)

        if health_status == "Needs Attention":
            st.warning(f"AI Prediction: {health_status}")
            st.write("Please monitor your symptoms and consider resting or consulting a doctor.")
        else:
            st.success(f"AI Prediction: {health_status}")
            st.write("Your health status looks normal today.")

        record = {
            "type": "health_check",
            "temperature": temperature,
            "feeling": feeling,
            "missed_doses": missed_doses,
            "health_status": health_status,
        }
        save_record(record)
        st.info("Data saved successfully.")


