import streamlit as st
from storage import load_history


def show():
    st.header("Medicine History")

    history = load_history()

    if not history:
        st.info("No records found yet.")
    else:
        for i, record in enumerate(reversed(history), start=1):
            st.write(f"**Record {len(history) - i + 1}** — Type: {record['type']}")
            st.json(record)
