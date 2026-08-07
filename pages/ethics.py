import streamlit as st
import pandas as pd
from datetime import date

from database.connection import SessionLocal
from database.models import AIModel, EthicsAssessment


st.title("⚖️ AI Model Ethics Assessment")


session = SessionLocal()


models = session.query(AIModel).all()


if not models:

    st.warning(
        "No AI models found. Please register a model first."
    )

else:

    st.subheader("Create Ethics Assessment")


    model_options = {
        model.model_name: model.id
        for model in models
    }


    selected_model = st.selectbox(
        "Select AI Model",
        list(model_options.keys())
    )


    bias_check = st.checkbox(
        "Bias Evaluation Completed"
    )


    fairness_check = st.checkbox(
        "Fairness Testing Completed"
    )


    explainability_check = st.checkbox(
        "Explainability Available"
    )


    human_review = st.checkbox(
        "Human Review Process Available"
    )


    if st.button("Generate Ethics Score"):


        score = 0


        if bias_check:
            score += 25


        if fairness_check:
            score += 25


        if explainability_check:
            score += 25


        if human_review:
            score += 25



        ethics = EthicsAssessment(

            model_id=model_options[selected_model],

            score=score,

            assessment_date=date.today()

        )


        session.add(ethics)

        session.commit()


        st.success(
            f"Ethics Score Generated: {score}%"
        )



st.subheader("Ethics Assessment History")


records = session.query(EthicsAssessment).all()


if records:

    data = []


    for e in records:

        model = session.query(AIModel).filter(
            AIModel.id == e.model_id
        ).first()


        data.append(
            {
                "Model": model.model_name,
                "Ethics Score": f"{e.score}%",
                "Date": e.assessment_date
            }
        )


    df = pd.DataFrame(data)


    st.dataframe(
        df,
        use_container_width=True
    )


else:

    st.info(
        "No ethics assessments found."
    )


session.close()