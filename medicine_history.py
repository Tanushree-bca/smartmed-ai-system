import streamlit as st
import pandas as pd
from storage import load_history


def build_health_table(history):
    rows = []
    for record in history:
        if record["type"] == "health_check":
            rows.append({
                "Date/Time Recorded": record.get("current_time", "-"),
                "Temperature (F)": record.get("temperature", "-"),
                "Feeling": record.get("feeling", "-"),
                "Health Status": record.get("health_status", "-"),
            })
    return rows


def build_medicine_table(history):
    rows = []
    for record in history:
        if record["type"] == "medicine":
            for med in record.get("medicines", []):
                rows.append({
                    "Recorded At": record.get("current_time", "-"),
                    "Medicine Name": med.get("name", "-"),
                    "Reminder Time": med.get("time", "-"),
                    "Taken?": med.get("taken", "-").capitalize(),
                })
    return rows


def show():
    st.header("Medicine History")

    history = load_history()

    if not history:
        st.info("No records found yet.")
        return

    st.subheader("Medicine Records")
    medicine_rows = build_medicine_table(history)
    if medicine_rows:
        df_medicine = pd.DataFrame(medicine_rows)
        st.table(df_medicine)
    else:
        st.info("No medicine records found yet.")

    st.subheader("Health Check Records")
    health_rows = build_health_table(history)
    if health_rows:
        df_health = pd.DataFrame(health_rows)
        st.table(df_health)
    else:
        st.info("No health check records found yet.")