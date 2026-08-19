import streamlit as st
import time
from storage import save_record


def show():
    st.header("Medicine Reminder")

    current_time = time.strftime("%I:%M %p")
    st.write("Current time:", current_time)

    medicines = []

    with st.form("medicine_form"):
        for i in range(1, 4):
            st.subheader(f"Medicine {i}")
            name = st.text_input(f"Medicine {i} name", key=f"name{i}")
            reminder_time = st.text_input(f"Medicine {i} time (e.g. 09:00 AM)", key=f"time{i}")
            taken = st.radio(f"Did you take Medicine {i}?", ["yes", "no"], key=f"taken{i}", horizontal=True)
            medicines.append({"name": name, "time": reminder_time, "taken": taken})

        submitted = st.form_submit_button("Submit")

    if submitted:
        missed_count = sum(1 for m in medicines if m["taken"] == "no")

        for m in medicines:
            if m["name"]:
                status = "missed" if m["taken"] == "no" else "taken"
                st.write(f"**{m['name']}** ({m['time']}) — Status: {status}")

        st.write("Total missed doses:", missed_count)
        if missed_count == 0:
            st.success("Great job! You are taking your medicines on time.")
        elif missed_count == 1:
            st.warning("You missed 1 dose. Try to be careful.")
        else:
            st.error(f"Warning: You have missed {missed_count} doses.")

        record = {
            "type": "medicine",
            "current_time": current_time,
            "medicines": medicines,
            "missed_count": missed_count,
        }
        save_record(record)
        st.info("Data saved successfully.")
