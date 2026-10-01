import streamlit as st
from storage import save_record
from reminder_utils import parse_time_str, is_due, generate_beep_base64, now_ist


def show():
    st.subheader("🏠 Medicine Reminder")
    st.write("Set your medicine times below. Click **Check My Reminders** anytime to see if it's time to take one.")

    current_time_str = now_ist().strftime("%I:%M %p")
    st.info(f"🕒 Current time: **{current_time_str}**")

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

        col_a, col_b = st.columns(2)
        with col_a:
            check_clicked = st.form_submit_button("🔔 Check My Reminders")
        with col_b:
            submitted = st.form_submit_button("✅ Submit & Save")

    # ---------- Reminder / Alarm check ----------
    if check_clicked:
        due_meds = []
        for m in medicines:
            if m["name"] and m["taken"] == "no":
                parsed = parse_time_str(m["time"])
                if parsed and is_due(parsed):
                    due_meds.append(m["name"])

        if due_meds:
            st.error(f"🔔⏰ **ALARM: It's time to take {', '.join(due_meds)}!**")
            beep_b64 = generate_beep_base64()
            st.markdown(
                f"""<audio autoplay>
                <source src="data:audio/wav;base64,{beep_b64}" type="audio/wav">
                </audio>""",
                unsafe_allow_html=True,
            )
        else:
            st.success("✅ No reminders due right now. You're all caught up!")

    # ---------- Save / Submit ----------
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
            "current_time": current_time_str,
            "medicines": medicines,
            "missed_count": missed_count,
        }
        save_record(record)
        st.toast("Data saved successfully ✅")
