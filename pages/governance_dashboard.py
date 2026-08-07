import streamlit as st
import pandas as pd

from database.connection import SessionLocal
from database.models import (
    AIModel,
    RiskAssessment,
    ComplianceAssessment,
    EthicsAssessment,
    Incident
)


st.title("🏢 AI Governance Executive Dashboard")


session = SessionLocal()


# Model Statistics

models = session.query(AIModel).all()

total_models = len(models)

high_risk_models = len(
    [
        m for m in models
        if m.risk_level == "High"
    ]
)


# Risk Statistics

risk_records = session.query(
    RiskAssessment
).all()


average_risk = 0

if risk_records:

    average_risk = round(
        sum(
            r.score for r in risk_records
        )
        /
        len(risk_records),
        2
    )



# Compliance Statistics

compliance_records = session.query(
    ComplianceAssessment
).all()


average_compliance = 0

if compliance_records:

    average_compliance = round(
        sum(
            c.score for c in compliance_records
        )
        /
        len(compliance_records),
        2
    )



# Ethics Statistics

ethics_records = session.query(
    EthicsAssessment
).all()


average_ethics = 0

if ethics_records:

    average_ethics = round(
        sum(
            e.score for e in ethics_records
        )
        /
        len(ethics_records),
        2
    )



# Incident Statistics

incidents = session.query(
    Incident
).all()


total_incidents = len(incidents)


open_incidents = len(
    [
        i for i in incidents
        if i.status == "Open"
    ]
)


resolved_incidents = len(
    [
        i for i in incidents
        if i.status == "Resolved"
    ]
)



# Display Cards

st.subheader("AI Model Overview")


col1, col2, col3 = st.columns(3)


col1.metric(
    "Total Models",
    total_models
)


col2.metric(
    "High Risk Models",
    high_risk_models
)


col3.metric(
    "Risk Score Average",
    average_risk
)



st.subheader("Governance Scores")


col4, col5, col6 = st.columns(3)


col4.metric(
    "Compliance Score",
    f"{average_compliance}%"
)


col5.metric(
    "Ethics Score",
    f"{average_ethics}%"
)


col6.metric(
    "Open Incidents",
    open_incidents
)



st.subheader("Incident Summary")


incident_df = pd.DataFrame(
    {
        "Status":
        [
            "Open",
            "Resolved"
        ],

        "Count":
        [
            open_incidents,
            resolved_incidents
        ]
    }
)


st.bar_chart(
    incident_df.set_index("Status")
)



session.close()