import streamlit as st
import medicine_reminder
import health_check
import medicine_history

st.set_page_config(
    page_title="SmartMed AI",
    page_icon="💊",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ---------- Custom styling ----------
st.markdown("""
<style>
    .stApp {
        background-color: #f5f9fc;
    }

    section[data-testid="stSidebar"] {
        background-color: #1b3a4b;
    }
    section[data-testid="stSidebar"] * {
        color: white !important;
    }

    .title-box {
        background: linear-gradient(90deg, #2193b0, #6dd5ed);
        padding: 25px;
        border-radius: 12px;
        margin-bottom: 25px;
        text-align: center;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
    }
    .title-box h1 {
        color: white;
        margin: 0;
        font-size: 32px;
    }
    .title-box p {
        color: #eafaff;
        margin: 5px 0 0 0;
        font-size: 15px;
    }

    div.stButton > button, div.stFormSubmitButton > button {
        background-color: #2193b0;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 8px 20px;
        font-weight: 600;
    }
    div.stButton > button:hover, div.stFormSubmitButton > button:hover {
        background-color: #176882;
        color: white;
    }

    /* Sidebar nav buttons */
    section[data-testid="stSidebar"] div.stButton > button {
        width: 100%;
        text-align: left;
        background-color: transparent;
        border: 1px solid transparent;
        font-weight: 500;
        padding: 10px 14px;
        margin-bottom: 4px;
    }
    section[data-testid="stSidebar"] div.stButton > button:hover {
        background-color: rgba(255,255,255,0.1);
        border: 1px solid rgba(255,255,255,0.3);
    }

    .block-container {
        padding-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# ---------- Sidebar navigation (buttons instead of radio for reliable mobile taps) ----------
if "page" not in st.session_state:
    st.session_state.page = "Medicine Reminder"

st.sidebar.markdown("## 💊 SmartMed AI")
st.sidebar.markdown("---")
st.sidebar.markdown("**Navigate**")

nav_items = [
    ("🏠 Medicine Reminder", "Medicine Reminder"),
    ("🩺 Health Check", "Health Check"),
    ("📋 Medicine History", "Medicine History"),
]

for label, key in nav_items:
    is_active = st.session_state.page == key
    prefix = "➤ " if is_active else "　"
    if st.sidebar.button(prefix + label, key=f"nav_{key}", use_container_width=True):
        st.session_state.page = key
        st.rerun()

st.sidebar.markdown("---")
st.sidebar.caption("AI + Cloud powered health assistant")

# ---------- Title banner ----------
st.markdown("""
<div class="title-box">
    <h1>💊 SmartMed AI System</h1>
    <p>Your AI-powered medicine reminder & health companion</p>
</div>
""", unsafe_allow_html=True)

# ---------- Page routing ----------
if st.session_state.page == "Medicine Reminder":
    medicine_reminder.show()
elif st.session_state.page == "Health Check":
    health_check.show()
elif st.session_state.page == "Medicine History":
    medicine_history.show()