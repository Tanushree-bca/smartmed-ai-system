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


def compute_compliance(history):
    taken = 0
    missed = 0
    for record in history:
        if record["type"] == "medicine":
            for med in record.get("medicines", []):
                if med.get("name"):
                    if med.get("taken") == "yes":
                        taken += 1
                    else:
                        missed += 1
    return taken, missed


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

    # ---------- Compliance Chart ----------
    taken, missed = compute_compliance(history)
    if taken + missed > 0:
        st.markdown("### 📊 Medicine Compliance Overview")
        compliance_pct = round((taken / (taken + missed)) * 100, 1)

        chart_col, score_col = st.columns([2, 1])
        with chart_col:
            chart_df = pd.DataFrame({"Doses": [taken, missed]}, index=["Taken ✅", "Missed ❌"])
            st.bar_chart(chart_df)
        with score_col:
            st.metric("Compliance Score", f"{compliance_pct}%")
            if compliance_pct >= 80:
                st.success("Great consistency! 🎉")
            elif compliance_pct >= 50:
                st.warning("Room for improvement.")
            else:
                st.error("Needs attention.")

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