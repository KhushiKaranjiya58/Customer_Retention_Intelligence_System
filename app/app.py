from utils import load_model
import pandas as pd
import matplotlib.pyplot as plt

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

col1, col2, col3 = st.columns([1,1,1], gap="large")

# ================= COLUMN 1 =================

with col1:

    st.markdown("### 👤 Customer Details")

    gender = st.selectbox(
        "Gender",
        ["Male", "Female"]
    )

    senior_citizen = st.selectbox(
        "Senior Citizen",
        ["Yes", "No"]
    )

    partner = st.selectbox(
        "Partner",
        ["Yes", "No"]
    )

    dependents = st.selectbox(
        "Dependents",
        ["Yes", "No"]
    )

    tenure = st.slider(
        "Tenure Months",
        1,
        72,
        12
    )
# ================= COLUMN 2 =================

with col2:

    st.markdown("### 🌐 Services")

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

# ================= COLUMN 3 =================

with col3:

    st.markdown("### 💳 Billing & Contract")

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

    monthly_charges = st.number_input(
        "Monthly Charges",
        min_value=0.0,
        value=50.0
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

c1, c2, c3 = st.columns([2,1,2])

with c2:
    predict = st.button(
        "🚀 Predict Churn",
        use_container_width=True
    )
        

if predict:

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

    # Risk Tier
    if probability >= 0.70:
        risk_tier = "High Risk"
    elif probability >= 0.40:
        risk_tier = "Medium Risk"
    else:
        risk_tier = "Low Risk"

    # Customer Segment
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

    # Priority Score
    retention_priority_score = (
        probability
        * cltv
        * (1 + (72 - tenure)/72)
    )

    # Recommendations
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

    st.divider()

    st.header("📈 Prediction Dashboard")

    r1, r2, r3, r4 = st.columns(4)

    with r1:
        st.metric(
            "Churn Probability",
            f"{probability*100:.2f}%"
        )

    with r2:
        st.metric(
            "Risk Tier",
            risk_tier
        )

    with r3:
        st.metric(
            "Customer Segment",
            segment
        )

    with r4:
        st.metric(
            "Priority Score",
            round(retention_priority_score, 2)
        )

    if risk_tier == "High Risk":
        st.error("🔴 High Risk Customer")

    elif risk_tier == "Medium Risk":
        st.warning("🟠 Medium Risk Customer")

    else:
        st.success("🟢 Low Risk Customer")

    st.subheader("Customer Risk Score")
    st.progress(int(probability * 100))

    st.subheader("📊 Churn Visualization")

    graph_col1, graph_col2 = st.columns([1, 1])

    with graph_col1:

        fig, ax = plt.subplots(figsize=(4,3))

        bars = ax.bar(
            ["Retain", "Churn"],
            [1-probability, probability]
        )

        for bar in bars:

            height = bar.get_height()

            ax.text(
                bar.get_x() + bar.get_width()/2,
                height,
                f"{height:.2f}",
                ha="center"
            )

        ax.set_ylabel("Probability")
        ax.set_title("Customer Churn Prediction")

        st.pyplot(fig)

    with graph_col2:

        st.info(f"Risk Tier: {risk_tier}")
        st.info(f"Customer Segment: {segment}")
        st.info(
            f"Priority Score: {round(retention_priority_score,2)}"
        )

    st.subheader("🎯 Retention Recommendations")

    for rec in recommendations:
        st.write("✅", rec)