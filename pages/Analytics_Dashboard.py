import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Analytics Dashboard",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Customer Analytics Dashboard")

df = pd.read_csv("data/processed_customer_data.csv")

# KPI Metrics

total_customers = len(df)

churn_rate = (
    df["Churn Value"].mean() * 100
)

avg_cltv = (
    df["CLTV"].mean()
)

high_risk = (
    df[df["Churn Value"] == 1].shape[0]
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Customers",
    total_customers
)

col2.metric(
    "Churn Rate",
    f"{churn_rate:.2f}%"
)

col3.metric(
    "Average CLTV",
    f"{avg_cltv:.0f}"
)

col4.metric(
    "Churn Customers",
    high_risk
)

import matplotlib.pyplot as plt

import matplotlib.pyplot as plt

# Prepare data

contract_churn = pd.crosstab(
    df["Contract"],
    df["Churn Value"]
)

internet_churn = pd.crosstab(
    df["Internet Service"],
    df["Churn Value"]
)

# Row 1

col1, col2 = st.columns(2)

with col1:
    st.subheader("Churn Distribution")

    fig, ax = plt.subplots(figsize=(4,3))

    df["Churn Value"].value_counts().plot(
        kind="bar",
        ax=ax
    )

    st.pyplot(fig)

with col2:
    st.subheader("Monthly Charges Distribution")

    fig, ax = plt.subplots(figsize=(4,3))

    ax.hist(
        df["Monthly Charges"],
        bins=20
    )

    st.pyplot(fig)

# Row 2

col1, col2 = st.columns(2)

with col1:
    st.subheader("Contract Type vs Churn")
    st.bar_chart(contract_churn)

with col2:
    st.subheader("Internet Service vs Churn")
    st.bar_chart(internet_churn)

st.header("Model Performance")

col1,col2,col3,col4,col5 = st.columns(5)

col1.metric("Accuracy","80.8%")
col2.metric("Precision","64.9%")
col3.metric("Recall","60.4%")
col4.metric("F1 Score","62.6%")
col5.metric("ROC-AUC","84.3%")

st.header("Business Insights")

st.success(
    """
    • Month-to-month customers show highest churn risk.

    • Low engagement customers require retention campaigns.

    • High CLTV customers should be prioritized.

    • Tech Support and Online Security reduce churn.
    """
)