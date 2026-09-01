import streamlit as st
import pandas as pd
from storage import load_history


def build_health_table(history):
    rows = []
    for record in history:
        if record["type"] == "health_check":
            rows.append({
                "🕒 Time": record.get("current_time", "-"),
                "🌡️ Temp (°F)": record.get("temperature", "-"),
                "😊 Feeling": record.get("feeling", "-"),
                "Status": record.get("health_status", "-"),
            })
    return rows


def build_medicine_table(history):
    rows = []
    for record in history:
        if record["type"] == "medicine":
            for med in record.get("medicines", []):
                if med.get("name"):
                    rows.append({
                        "🕒 Recorded At": record.get("current_time", "-"),
                        "💊 Medicine": med.get("name", "-"),
                        "⏰ Reminder Time": med.get("time", "-"),
                        "Status": "✅ Taken" if med.get("taken") == "yes" else "❌ Missed",
                    })
    return rows


def show():
    st.subheader("📋 Medicine History")
    st.write("A complete record of your medicines and health checks.")

    history = load_history()

    if not history:
        st.info("No records found yet. Start by adding a medicine or doing a health check!")
        return

    total_medicine_records = len([r for r in history if r["type"] == "medicine"])
    total_health_records = len([r for r in history if r["type"] == "health_check"])

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Records", len(history))
    col2.metric("Medicine Logs", total_medicine_records)
    col3.metric("Health Checks", total_health_records)

    st.markdown("---")

    tab1, tab2 = st.tabs(["💊 Medicine Records", "🩺 Health Check Records"])

    with tab1:
        medicine_rows = build_medicine_table(history)
        if medicine_rows:
            df_medicine = pd.DataFrame(medicine_rows)
            st.dataframe(df_medicine, use_container_width=True, hide_index=True)
        else:
            st.info("No medicine records found yet.")

    with tab2:
        health_rows = build_health_table(history)
        if health_rows:
            df_health = pd.DataFrame(health_rows)
            st.dataframe(df_health, use_container_width=True, hide_index=True)
        else:
            st.info("No health check records found yet.")