import streamlit as st
import pandas as pd

from database.connection import SessionLocal
from database.models import Incident


st.title("📊 Incident Dashboard")


session = SessionLocal()


incidents = session.query(Incident).all()


if incidents:

    df = pd.DataFrame(
        [
            {
                "Severity": i.severity,
                "Status": i.status,
                "Date": i.incident_date
            }
            for i in incidents
        ]
    )


    # Total Incidents

    st.subheader("Overview")

    col1, col2, col3 = st.columns(3)


    col1.metric(
        "Total Incidents",
        len(df)
    )


    col2.metric(
        "Open Incidents",
        len(
            df[df["Status"] == "Open"]
        )
    )


    col3.metric(
        "Resolved Incidents",
        len(
            df[df["Status"] == "Resolved"]
        )
    )



    # Severity Chart

    st.subheader("Severity Distribution")


    severity_count = (
        df["Severity"]
        .value_counts()
    )


    st.bar_chart(
        severity_count
    )



    # Status Chart

    st.subheader("Status Distribution")


    status_count = (
        df["Status"]
        .value_counts()
    )


    st.bar_chart(
        status_count
    )


else:

    st.info(
        "No incident data available"
    )


session.close()