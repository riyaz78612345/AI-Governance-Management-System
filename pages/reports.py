import streamlit as st
import pandas as pd
from io import BytesIO

from database.connection import SessionLocal
from database.models import AIModel
from utils.pdf_report import generate_pdf

st.title("📄 Reports")

st.write("Generate and download AI Governance reports.")

session = SessionLocal()

models = session.query(AIModel).all()

if models:

    df = pd.DataFrame(
        [
            {
                "ID": m.id,
                "Model Name": m.model_name,
                "Owner": m.owner,
                "Department": m.department,
                "Purpose": m.purpose,
                "Dataset": m.dataset,
                "Version": m.version,
                "Status": m.status,
                "Risk Level": m.risk_level,
                "Deployment Date": m.deployment_date,
            }
            for m in models
        ]
    )

    st.subheader("Registered AI Models")

    st.dataframe(df, use_container_width=True)

    output = BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="AI Models")

    excel_data = output.getvalue()

    st.download_button(
        label="📥 Download Excel Report",
        data=excel_data,
        file_name="AI_Models_Report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    pdf_buffer = generate_pdf(df)

    st.download_button(
    label="📄 Download PDF Report",
    data=pdf_buffer,
    file_name="AI_Models_Report.pdf",
    mime="application/pdf",
)

else:
    st.info("No AI models available to generate a report.")

session.close()