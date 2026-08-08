import streamlit as st

from database.connection import SessionLocal
from database.models import User
from utils.security import verify_password


def login():

    st.title("🔐 AI Governance Login")

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        session = SessionLocal()

        user = session.query(User).filter(
            User.username == username
        ).first()

        if user and verify_password(password, user.password):

            st.session_state.logged_in = True
            st.session_state.username = user.username
            st.session_state.role = user.role

            session.close()

            st.success("Login Successful!")

            st.rerun()

        else:

            session.close()

            st.error("Invalid Username or Password")