import streamlit as st
def load_css():
    with open("assets/style.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

from database.connection import engine
from database.models import Base
from auth.login import login

# Create database tables
Base.metadata.create_all(bind=engine)

# Page configuration
st.set_page_config(
    page_title="AI Governance Management System",
    page_icon="🛡️",
    layout="wide"
)

load_css()

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "role" not in st.session_state:
    st.session_state.role = ""

# Show login page
if not st.session_state.logged_in:
    login()
    st.stop()

# Sidebar
st.sidebar.title("🛡️ AI Governance")

st.sidebar.success(f"Welcome, {st.session_state.username}")

st.sidebar.write(f"Role: {st.session_state.role}")

if st.sidebar.button("🚪 Logout"):

    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""

    st.rerun()

# Main Dashboard

st.title("🛡️ AI Governance Management System")

st.subheader("Enterprise AI Governance Dashboard")

st.success("Database connected successfully!")

st.write("Welcome to the AI Governance Management System.")

col1, col2, col3 = st.columns(3)

col1.metric("AI Models", "0")

col2.metric("High Risk Models", "0")

col3.metric("Compliance Score", "100%")