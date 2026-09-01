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
    /* Main background */
    .stApp {
        background-color: #f5f9fc;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #1b3a4b;
    }
    section[data-testid="stSidebar"] * {
        color: white !important;
    }

    /* Title area */
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

    /* Buttons */
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

    /* Cards / containers */
    .block-container {
        padding-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# ---------- Sidebar ----------
st.sidebar.markdown("## 💊 SmartMed AI")
st.sidebar.markdown("---")
page = st.sidebar.radio("Navigate", ["🏠 Medicine Reminder", "🩺 Health Check", "📋 Medicine History"])
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
if page == "🏠 Medicine Reminder":
    medicine_reminder.show()
elif page == "🩺 Health Check":
    health_check.show()
elif page == "📋 Medicine History":
    medicine_history.show()
