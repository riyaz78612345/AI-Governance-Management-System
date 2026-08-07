import streamlit as st
import pandas as pd

from database.connection import SessionLocal
from database.models import User
from utils.security import hash_password

if "logged_in" not in st.session_state:
    st.error("Please login first.")
    st.stop()

if st.session_state.role != "Admin":
    st.error("⛔ Access Denied")
    st.warning("Only administrators can access this page.")
    st.stop()

st.title("👥 User Management")

st.write("Manage users and their roles.")

session = SessionLocal()

# -----------------------------
# Add New User
# -----------------------------

st.subheader("➕ Add New User")

with st.form("user_form"):

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    role = st.selectbox(
        "Role",
        [
            "Admin",
            "Compliance Officer",
            "Auditor",
            "Viewer"
        ]
    )

    submit = st.form_submit_button("Create User")

if submit:

    existing_user = (
        session.query(User)
        .filter(User.username == username)
        .first()
    )

    if existing_user:

        st.error("Username already exists.")

    else:

        user = User(
            username=username,
            password=hash_password(password),
            role=role
        )

        session.add(user)
        session.commit()

        st.success("User created successfully!")

# -----------------------------
# Display Users
# -----------------------------

users = session.query(User).all()

if users:

    df = pd.DataFrame(
        [
            {
                "ID": u.id,
                "Username": u.username,
                "Role": u.role
            }
            for u in users
        ]
    )

    st.divider()

    st.subheader("Registered Users")

    st.dataframe(df, use_container_width=True)

    # -----------------------------
    # Edit/Delete User
    # -----------------------------

    st.divider()

    st.subheader("Manage Existing Users")

    selected_id = st.selectbox(
        "Select User",
        df["ID"]
    )

    selected_user = (
        session.query(User)
        .filter(User.id == selected_id)
        .first()
    )

    if selected_user:

        new_username = st.text_input(
            "Username",
            value=selected_user.username
        )

        new_role = st.selectbox(
            "Role",
            [
                "Admin",
                "Compliance Officer",
                "Auditor",
                "Viewer"
            ],
            index=[
                "Admin",
                "Compliance Officer",
                "Auditor",
                "Viewer"
            ].index(selected_user.role)
        )

        col1, col2 = st.columns(2)

        with col1:

            if st.button("✏️ Update User"):

                selected_user.username = new_username
                selected_user.role = new_role

                session.commit()

                st.success("User updated successfully!")

                st.rerun()

        with col2:

            if st.button("🗑️ Delete User"):

                session.delete(selected_user)

                session.commit()

                st.success("User deleted successfully!")

                st.rerun()

session.close()