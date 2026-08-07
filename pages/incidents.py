import streamlit as st
import pandas as pd
from datetime import date

from database.connection import SessionLocal
from database.models import Incident


st.title("🚨 Incident Management")

session = SessionLocal()


# ---------------- CREATE INCIDENT ----------------

st.subheader("Create New Incident")

with st.form("incident_form"):

    model_name = st.text_input("Affected Model Name")

    description = st.text_area("Description")

    severity = st.selectbox(
        "Severity",
        ["Low", "Medium", "High", "Critical"]
    )

    status = st.selectbox(
        "Status",
        ["Open", "In Progress", "Resolved"]
    )

    assigned_to = st.text_input("Reported By")

    submit = st.form_submit_button("Create Incident")


if submit:

    incident = Incident(
        model_name=model_name,
        description=description,
        severity=severity,
        reported_by=assigned_to,
        status=status,
        incident_date=date.today()
    )

    session.add(incident)
    session.commit()

    st.success("✅ Incident created successfully!")


# ---------------- VIEW INCIDENTS ----------------

incidents = session.query(Incident).all()


st.subheader("Incident List")


if incidents:

    df = pd.DataFrame(
        [
            {
                "ID": i.id,
                "Model": i.model_name,
                "Description": i.description,
                "Severity": i.severity,
                "Status": i.status,
                "Reported By": i.reported_by,
                "Date": i.incident_date
            }
            for i in incidents
        ]
    )

    st.dataframe(
        df,
        use_container_width=True
    )

else:

    st.info("No incidents found.")



# ---------------- UPDATE STATUS ----------------

st.subheader("Update Incident Status")


if incidents:

    incident_options = {
        f"{i.id} - {i.model_name}": i.id
        for i in incidents
    }


    selected_incident = st.selectbox(
        "Select Incident",
        list(incident_options.keys())
    )


    new_status = st.selectbox(
        "Change Status To",
        [
            "Open",
            "In Progress",
            "Resolved",
            "Closed"
        ]
    )


    if st.button("Update Status"):

        incident_id = incident_options[selected_incident]


        incident = session.query(Incident).filter(
            Incident.id == incident_id
        ).first()


        incident.status = new_status

        session.commit()


        st.success(
            "✅ Incident status updated successfully!"
        )

        st.rerun()



# ---------------- DELETE INCIDENT ----------------

st.subheader("Delete Incident")


if incidents:

    delete_options = {
        f"{i.id} - {i.model_name}": i.id
        for i in incidents
    }


    selected_delete = st.selectbox(
        "Select Incident To Delete",
        list(delete_options.keys())
    )


    if st.button("Delete Incident"):

        incident_id = delete_options[selected_delete]


        incident = session.query(Incident).filter(
            Incident.id == incident_id
        ).first()


        session.delete(incident)

        session.commit()


        st.success(
            "🗑️ Incident deleted successfully!"
        )

        st.rerun()



session.close()