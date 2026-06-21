from utils import load_model
import pandas as pd

model = load_model()

import streamlit as st

st.set_page_config(
    page_title="Customer Retention Intelligence System",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Customer Retention Intelligence System")

st.success("Model Loaded Successfully ✅")

st.header("Customer Information")

gender = st.selectbox(
    "Gender",
    ["Male", "Female"]
)

tenure = st.slider(
    "Tenure Months",
    1,
    72,
    12
)

monthly_charges = st.number_input(
    "Monthly Charges",
    min_value=0.0,
    value=50.0
)


senior_citizen = st.selectbox("Senior Citizen", ["Yes", "No"])

partner = st.selectbox("Partner", ["Yes", "No"])

dependents = st.selectbox("Dependents", ["Yes", "No"])

phone_service = st.selectbox(
    "Phone Service",
    ["Yes", "No"]
)

multiple_lines = st.selectbox(
    "Multiple Lines",
    ["Yes", "No", "No phone service"]
)

internet_service = st.selectbox(
    "Internet Service",
    ["DSL", "Fiber optic", "No"]
)

online_security = st.selectbox(
    "Online Security",
    ["Yes", "No", "No internet service"]
)

online_backup = st.selectbox(
    "Online Backup",
    ["Yes", "No", "No internet service"]
)

device_protection = st.selectbox(
    "Device Protection",
    ["Yes", "No", "No internet service"]
)

tech_support = st.selectbox(
    "Tech Support",
    ["Yes", "No", "No internet service"]
)

streaming_tv = st.selectbox(
    "Streaming TV",
    ["Yes", "No", "No internet service"]
)

streaming_movies = st.selectbox(
    "Streaming Movies",
    ["Yes", "No", "No internet service"]
)

contract = st.selectbox(
    "Contract",
    ["Month-to-month", "One year", "Two year"]
)

paperless_billing = st.selectbox(
    "Paperless Billing",
    ["Yes", "No"]
)

payment_method = st.selectbox(
    "Payment Method",
    [
        "Electronic check",
        "Mailed check",
        "Bank transfer (automatic)",
        "Credit card (automatic)"
    ]
)

cltv = st.number_input(
    "CLTV",
    min_value=2000,
    max_value=7000,
    value=4000
)

engagement_score = st.slider(
    "Engagement Score",
    0,
    6,
    3
)

if st.button("Predict Churn"):

    customer_data = pd.DataFrame({
        "Gender": [gender],
        "Senior Citizen": [senior_citizen],
        "Partner": [partner],
        "Dependents": [dependents],
        "Tenure Months": [tenure],
        "Phone Service": [phone_service],
        "Multiple Lines": [multiple_lines],
        "Internet Service": [internet_service],
        "Online Security": [online_security],
        "Online Backup": [online_backup],
        "Device Protection": [device_protection],
        "Tech Support": [tech_support],
        "Streaming TV": [streaming_tv],
        "Streaming Movies": [streaming_movies],
        "Contract": [contract],
        "Paperless Billing": [paperless_billing],
        "Payment Method": [payment_method],
        "Monthly Charges": [monthly_charges],
        "Total Charges": [tenure * monthly_charges],
        "CLTV": [cltv],
        "Engagement Score": [engagement_score]
    })

    probability = model.predict_proba(customer_data)[0][1]

    st.write("Churn Probability:", probability)

    if probability >= 0.70:
        risk_tier = "High Risk"
    elif probability >= 0.40:
        risk_tier = "Medium Risk"
    else:
        risk_tier = "Low Risk"

    st.write("Risk Tier:", risk_tier)

    if tenure <= 12 and probability >= 0.60:
        segment = "New Customer At-Risk"

    elif cltv >= 5000 and probability >= 0.60:
        segment = "Valuable At-Risk"

    elif monthly_charges >= 80 and contract == "Month-to-month":
        segment = "Price Sensitive"

    elif engagement_score <= 2:
        segment = "Low Engagement At-Risk"

    else:
        segment = "Loyal Customer"

    st.write("Customer Segment:", segment)

    retention_priority_score = (
        probability
        * cltv
        * (1 + (72 - tenure)/72)
    )

    st.write(
        "Retention Priority Score:",
        round(retention_priority_score, 2)
    )

    recommendations = []

    if probability >= 0.70:

        if contract == "Month-to-month":
            recommendations.append("Offer annual plan discount")

        if tech_support == "No":
            recommendations.append("Provide free tech support trial")

        if online_security == "No":
            recommendations.append("Offer security package")

        if engagement_score <= 2:
            recommendations.append("Launch engagement campaign")

        recommendations.append("Assign retention specialist")

    elif probability >= 0.40:

        if contract == "Month-to-month":
            recommendations.append("Offer annual plan discount")

        if engagement_score <= 2:
            recommendations.append("Launch engagement campaign")

    else:

        recommendations.append(
            "Customer is healthy. Maintain loyalty program."
        )
    st.subheader("Retention Recommendations")

    for rec in recommendations:
        st.write("✅", rec)