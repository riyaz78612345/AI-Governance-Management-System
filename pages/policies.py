import streamlit as st
import pandas as pd
from datetime import date, timedelta

from database.connection import SessionLocal
from database.models import Policy
from auth.permissions import has_permission

if not has_permission(st.session_state.role, "Policies"):
    st.error("❌ Access Denied")
    st.stop()

st.title("📘 AI Policy Management")

session = SessionLocal()

with st.form("policy_form"):

    policy_name = st.text_input("Policy Name")

    owner = st.text_input("Policy Owner")

    category = st.selectbox(
        "Category",
        [
            "AI Governance",
            "Data Privacy",
            "Security",
            "Ethics",
            "Compliance"
        ]
    )

    effective_date = st.date_input(
        "Effective Date",
        value=date.today()
    )

    review_date = st.date_input(
        "Review Date",
        value=date.today() + timedelta(days=365)
    )

    status = st.selectbox(
        "Status",
        [
            "Active",
            "Under Review",
            "Archived"
        ]
    )

    submit = st.form_submit_button("Save Policy")

if submit:

    policy = Policy(
        policy_name=policy_name,
        owner=owner,
        category=category,
        effective_date=effective_date,
        review_date=review_date,
        status=status
    )

    session.add(policy)
    session.commit()

    st.success("✅ Policy Saved Successfully")

policies = session.query(Policy).all()

if policies:

    df = pd.DataFrame([
        {
            "ID": p.id,
            "Policy": p.policy_name,
            "Owner": p.owner,
            "Category": p.category,
            "Status": p.status,
            "Review Date": p.review_date
        }
        for p in policies
    ])

    st.subheader("Policy Register")

    st.dataframe(df, use_container_width=True)

else:
    st.info("No policies available.")

session.close()