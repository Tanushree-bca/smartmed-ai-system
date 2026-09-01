import streamlit as st
import time
from storage import save_record


def show():
    st.subheader("🏠 Medicine Reminder")
    st.write("Track your daily medicines and mark them as taken or missed.")

    current_time = time.strftime("%I:%M %p")
    st.info(f"🕒 Current time: **{current_time}**")

    medicines = []

    with st.form("medicine_form"):
        cols = st.columns(3)
        for i in range(1, 4):
            with cols[i - 1]:
                st.markdown(f"**💊 Medicine {i}**")
                name = st.text_input(f"Name", key=f"name{i}", placeholder="e.g. Paracetamol")
                reminder_time = st.text_input(f"Time", key=f"time{i}", placeholder="e.g. 09:00 AM")
                taken = st.radio("Taken?", ["yes", "no"], key=f"taken{i}", horizontal=True)
                medicines.append({"name": name, "time": reminder_time, "taken": taken})

        submitted = st.form_submit_button("✅ Submit")

    if submitted:
        missed_count = sum(1 for m in medicines if m["taken"] == "no")

        st.markdown("### Summary")
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Medicines", len([m for m in medicines if m["name"]]))
        col2.metric("Taken", len(medicines) - missed_count)
        col3.metric("Missed", missed_count)

        for m in medicines:
            if m["name"]:
                if m["taken"] == "no":
                    st.warning(f"❌ **{m['name']}** ({m['time']}) — Missed")
                else:
                    st.success(f"✅ **{m['name']}** ({m['time']}) — Taken")

        if missed_count == 0:
            st.balloons()
            st.success("🎉 Great job! You are taking your medicines on time.")
        elif missed_count == 1:
            st.warning("⚠️ You missed 1 dose. Try to be careful.")
        else:
            st.error(f"🚨 Warning: You have missed {missed_count} doses.")

        record = {
            "type": "medicine",
            "current_time": current_time,
            "medicines": medicines,
            "missed_count": missed_count,
        }
        save_record(record)
        st.toast("Data saved successfully ✅")
