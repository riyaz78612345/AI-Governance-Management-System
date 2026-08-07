import streamlit as st
import pandas as pd
from datetime import date

from database.connection import SessionLocal
from database.models import Audit
from auth.permissions import has_permission

if not has_permission(st.session_state.role, "Audits"):
    st.error("❌ Access Denied")
    st.stop()

st.title("🔍 AI Audit Management")

session = SessionLocal()

with st.form("audit_form"):

    audit_name = st.text_input("Audit Name")

    auditor = st.text_input("Auditor")

    audit_type = st.selectbox(
        "Audit Type",
        [
            "Internal",
            "External",
            "Regulatory"
        ]
    )

    audit_date = st.date_input(
        "Audit Date",
        value=date.today()
    )

    findings = st.text_area("Key Findings")

    status = st.selectbox(
        "Status",
        [
            "Planned",
            "In Progress",
            "Completed"
        ]
    )

    submit = st.form_submit_button("Save Audit")

if submit:

    audit = Audit(
        audit_name=audit_name,
        auditor=auditor,
        audit_type=audit_type,
        audit_date=audit_date,
        findings=findings,
        status=status
    )

    session.add(audit)
    session.commit()

    st.success("✅ Audit Saved Successfully")

audits = session.query(Audit).all()

if audits:

    df = pd.DataFrame([
        {
            "ID": a.id,
            "Audit": a.audit_name,
            "Auditor": a.auditor,
            "Type": a.audit_type,
            "Date": a.audit_date,
            "Status": a.status
        }
        for a in audits
    ])

    st.subheader("Audit Register")

    st.dataframe(df, use_container_width=True)

else:
    st.info("No audits available.")

session.close()