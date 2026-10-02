import streamlit as st
from storage import save_record
from reminder_utils import is_due, generate_beep_bytes, now_ist


def show():
    st.subheader("🏠 Medicine Reminder")

    st.markdown("#### 👨‍👩‍👧 Step 1: Caregiver Setup (done once by a family member)")
    st.caption("Set the medicine name and time using the clock picker below — no typing needed for time.")

    current_dt = now_ist()
    st.info(f"🕒 Current time: **{current_dt.strftime('%I:%M %p')}**")

    medicines = []

    with st.form("medicine_form"):
        cols = st.columns(3)
        for i in range(1, 4):
            with cols[i - 1]:
                st.markdown(f"**💊 Medicine {i}**")
                name = st.text_input("Name", key=f"name{i}", placeholder="e.g. Paracetamol")
                reminder_time = st.time_input("Time", key=f"time{i}", value=None)
                medicines.append({"name": name, "time": reminder_time})

        save_schedule = st.form_submit_button("💾 Save Schedule")

    if save_schedule:
        st.success("Schedule saved! The person taking medicine can now just check below.")
        for m in medicines:
            if m["name"] and m["time"]:
                m_display = m["time"].strftime("%I:%M %p")
                st.write(f"✅ **{m['name']}** set for **{m_display}**")
        record = {
            "type": "medicine_schedule",
            "set_at": current_dt.strftime("%I:%M %p"),
            "medicines": [
                {"name": m["name"], "time": m["time"].strftime("%I:%M %p")}
                for m in medicines if m["name"] and m["time"]
            ],
        }
        save_record(record)
        st.toast("Schedule saved ✅")

    st.markdown("---")
    st.markdown("#### 👵 Step 2: For the Person Taking Medicine")
    st.caption("Just press the big button below — no typing or forms needed.")

    big_check = st.button("🔔 IS IT TIME FOR MY MEDICINE?", use_container_width=True, type="primary")

    if big_check:
        due_meds = []
        for m in medicines:
            if m["name"] and m["time"] and is_due(m["time"]):
                due_meds.append(m["name"])

        if due_meds:
            st.error(f"### 🔔⏰ YES! Time to take: {', '.join(due_meds)}")
            beep_audio = generate_beep_bytes()
            st.audio(beep_audio, format="audio/wav", autoplay=True)
            st.write("🔊 If you don't hear anything, tap the play button above.")

            taken_now = st.button(f"✅ I Took My Medicine", use_container_width=True)
            if taken_now:
                record = {
                    "type": "medicine",
                    "current_time": current_dt.strftime("%I:%M %p"),
                    "medicines": [{"name": n, "time": "-", "taken": "yes"} for n in due_meds],
                    "missed_count": 0,
                }
                save_record(record)
                st.success("Great! Recorded as taken. 🎉")
                st.balloons()
        else:
            st.success("✅ No, nothing due right now. Relax!")
