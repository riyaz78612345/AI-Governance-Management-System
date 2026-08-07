import streamlit as st
import pandas as pd
from datetime import date

from database.connection import SessionLocal
from database.models import AIModel, ComplianceAssessment


st.title("📋 AI Model Compliance Assessment")


session = SessionLocal()


models = session.query(AIModel).all()


if not models:

    st.warning(
        "No AI models found. Please register a model first."
    )

else:

    st.subheader("Create Compliance Assessment")


    model_options = {
        model.model_name: model.id
        for model in models
    }


    selected_model = st.selectbox(
        "Select AI Model",
        list(model_options.keys())
    )


    documentation = st.checkbox(
        "Model Documentation Available"
    )


    privacy = st.checkbox(
        "Privacy Review Completed"
    )


    explainability = st.checkbox(
        "Explainability Check Completed"
    )


    monitoring = st.checkbox(
        "Model Monitoring Enabled"
    )


    if st.button("Generate Compliance Score"):


        score = 0


        if documentation:
            score += 25


        if privacy:
            score += 25


        if explainability:
            score += 25


        if monitoring:
            score += 25



        compliance = ComplianceAssessment(

            model_id=model_options[selected_model],

            score=score,

            assessment_date=date.today()

        )


        session.add(compliance)

        session.commit()


        st.success(
            f"Compliance Score Generated: {score}%"
        )



st.subheader("Compliance History")


records = session.query(ComplianceAssessment).all()


if records:


    data = []


    for c in records:


        model = session.query(AIModel).filter(
            AIModel.id == c.model_id
        ).first()


        data.append(
            {
                "Model": model.model_name,
                "Compliance Score": f"{c.score}%",
                "Date": c.assessment_date
            }
        )


    df = pd.DataFrame(data)


    st.dataframe(
        df,
        use_container_width=True
    )


else:

    st.info(
        "No compliance assessments found."
    )


session.close()