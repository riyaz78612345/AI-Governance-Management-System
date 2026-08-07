import streamlit as st
import pandas as pd
from datetime import date

from auth.permissions import has_permission
from database.connection import SessionLocal
from database.models import AIModel

if not has_permission(st.session_state.role, "Model Registry"):
    st.error("❌ Access Denied")
    st.stop()

st.title("🤖 AI Model Registry")
st.write("Register AI models used in your organization.")

session = SessionLocal()

# ----------------------------
# Register New Model
# ----------------------------

with st.form("model_form"):

    model_name = st.text_input("Model Name")

    owner = st.text_input("Owner")

    department = st.selectbox(
        "Department",
        [
            "HR",
            "Finance",
            "Healthcare",
            "Sales",
            "Operations",
            "IT"
        ]
    )

    purpose = st.text_area("Purpose")

    dataset = st.text_input("Dataset Used")

    version = st.text_input("Version")

    status = st.selectbox(
        "Status",
        [
            "Development",
            "Testing",
            "Production"
        ]
    )

    risk_level = st.selectbox(
        "Risk Level",
        [
            "Low",
            "Medium",
            "High"
        ]
    )

    deployment_date = st.date_input(
        "Deployment Date",
        value=date.today()
    )

    submit = st.form_submit_button("Register Model")

if submit:

    model = AIModel(
        model_name=model_name,
        owner=owner,
        department=department,
        purpose=purpose,
        dataset=dataset,
        version=version,
        status=status,
        risk_level=risk_level,
        deployment_date=deployment_date
    )

    session.add(model)
    session.commit()

    st.success("✅ AI Model Registered Successfully!")

# ----------------------------
# Display Models
# ----------------------------

models = session.query(AIModel).all()

if models:

    df = pd.DataFrame([
        {
            "ID": m.id,
            "Model": m.model_name,
            "Owner": m.owner,
            "Department": m.department,
            "Status": m.status,
            "Risk": m.risk_level
        }
        for m in models
    ])

    st.subheader("📋 Registered AI Models")
    st.dataframe(df, use_container_width=True)

    st.divider()

    # ----------------------------
    # Update / Delete
    # ----------------------------

    st.subheader("✏️ Manage Models")

    selected_id = st.selectbox(
        "Select Model",
        df["ID"]
    )

    selected_model = session.query(AIModel).filter(
        AIModel.id == selected_id
    ).first()

    if selected_model:

        with st.form("edit_model"):

            new_name = st.text_input(
                "Model Name",
                value=selected_model.model_name
            )

            new_owner = st.text_input(
                "Owner",
                value=selected_model.owner
            )

            new_department = st.selectbox(
                "Department",
                [
                    "HR",
                    "Finance",
                    "Healthcare",
                    "Sales",
                    "Operations",
                    "IT"
                ],
                index=[
                    "HR",
                    "Finance",
                    "Healthcare",
                    "Sales",
                    "Operations",
                    "IT"
                ].index(selected_model.department)
            )

            new_purpose = st.text_area(
                "Purpose",
                value=selected_model.purpose
            )

            new_dataset = st.text_input(
                "Dataset",
                value=selected_model.dataset
            )

            new_version = st.text_input(
                "Version",
                value=selected_model.version
            )

            new_status = st.selectbox(
                "Status",
                [
                    "Development",
                    "Testing",
                    "Production"
                ],
                index=[
                    "Development",
                    "Testing",
                    "Production"
                ].index(selected_model.status)
            )

            new_risk = st.selectbox(
                "Risk Level",
                [
                    "Low",
                    "Medium",
                    "High"
                ],
                index=[
                    "Low",
                    "Medium",
                    "High"
                ].index(selected_model.risk_level)
            )

            new_date = st.date_input(
                "Deployment Date",
                value=selected_model.deployment_date
            )

            col1, col2 = st.columns(2)

            with col1:
                update = st.form_submit_button("✅ Update Model")

            with col2:
                delete = st.form_submit_button("🗑 Delete Model")

        if update:

            selected_model.model_name = new_name
            selected_model.owner = new_owner
            selected_model.department = new_department
            selected_model.purpose = new_purpose
            selected_model.dataset = new_dataset
            selected_model.version = new_version
            selected_model.status = new_status
            selected_model.risk_level = new_risk
            selected_model.deployment_date = new_date

            session.commit()

            st.success("✅ Model Updated Successfully!")
            st.rerun()

        if delete:

            session.delete(selected_model)
            session.commit()

            st.success("✅ Model Deleted Successfully!")
            st.rerun()

else:

    st.info("No AI Models Registered Yet.")

session.close()