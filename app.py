import streamlit as st
import medicine_reminder
import health_check
import medicine_history

st.set_page_config(page_title="SmartMed AI", page_icon="💊", layout="centered")

st.sidebar.title("SmartMed AI System")
page = st.sidebar.radio("Go to", ["Medicine Reminder", "Health Check", "Medicine History"])

st.title("💊 SmartMed AI System")

if page == "Medicine Reminder":
    medicine_reminder.show()
elif page == "Health Check":
    health_check.show()
elif page == "Medicine History":
    medicine_history.show()
