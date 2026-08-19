import streamlit as st
from storage import save_record


def get_health_status(temperature, feeling):
    if temperature > 100.4:
        return "Needs Attention", "Warning: You have a fever. Please monitor your temperature."
    elif feeling.lower() == "sick":
        return "Needs Attention", "You reported feeling sick. Please rest and monitor your symptoms."
    elif feeling.lower() == "tired":
        return "Needs Attention", "You reported feeling tired. Make sure you get enough rest."
    else:
        return "Normal", "Your health status looks normal today."


def show():
    st.header("Health Check")

    temperature = st.number_input("Body temperature (°F)", min_value=90.0, max_value=110.0, value=98.6, step=0.1)
    feeling = st.selectbox("How are you feeling today?", ["good", "tired", "sick"])

    if st.button("Check Health Status"):
        health_status, message = get_health_status(temperature, feeling)

        if health_status == "Needs Attention":
            st.warning(message)
        else:
            st.success(message)

        st.write("Health Status:", health_status)

        record = {
            "type": "health_check",
            "temperature": temperature,
            "feeling": feeling,
            "health_status": health_status,
        }
        save_record(record)
        st.info("Data saved successfully.")
