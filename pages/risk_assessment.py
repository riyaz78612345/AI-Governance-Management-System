import streamlit as st
import pandas as pd
from datetime import date

from database.connection import SessionLocal
from database.models import AIModel, RiskAssessment


st.title("⚠️ AI Model Risk Assessment")


session = SessionLocal()


# Get registered models

models = session.query(AIModel).all()


if not models:

    st.warning(
        "No AI models found. Please add models first."
    )

else:

    st.subheader("Create Risk Assessment")


    model_options = {
        model.model_name: model.id
        for model in models
    }


    selected_model = st.selectbox(
        "Select AI Model",
        list(model_options.keys())
    )


    personal_data = st.checkbox(
        "Uses Personal Data"
    )


    automated_decision = st.checkbox(
        "Automated Decision Making"
    )


    biometric_data = st.checkbox(
        "Uses Biometric Data"
    )


    human_oversight = st.checkbox(
        "Human Oversight Available"
    )


    employment = st.checkbox(
        "Employment Related"
    )


    if st.button("Calculate Risk"):


        score = 0


        if personal_data:
            score += 20

        if automated_decision:
            score += 20

        if biometric_data:
            score += 25

        if not human_oversight:
            score += 20

        if employment:
            score += 15



        if score >= 70:
            level = "High"

        elif score >= 40:
            level = "Medium"

        else:
            level = "Low"



        risk = RiskAssessment(

            model_id=model_options[selected_model],

            personal_data=personal_data,

            automated_decision=automated_decision,

            biometric_data=biometric_data,

            human_oversight=human_oversight,

            employment=employment,

            score=score,

            level=level,

            assessment_date=date.today()
        )


        session.add(risk)

        session.commit()


        st.success(
            f"Risk Assessment Completed. Score: {score} ({level})"
        )



# Display existing assessments


st.subheader("Risk Assessment History")


assessments = session.query(RiskAssessment).all()


if assessments:


    data=[]


    for r in assessments:

        model = session.query(AIModel).filter(
            AIModel.id == r.model_id
        ).first()


        data.append(
            {
                "Model": model.model_name,
                "Score": r.score,
                "Level": r.level,
                "Date": r.assessment_date
            }
        )


    df = pd.DataFrame(data)


    st.dataframe(
        df,
        use_container_width=True
    )


else:

    st.info(
        "No assessments available"
    )


session.close()