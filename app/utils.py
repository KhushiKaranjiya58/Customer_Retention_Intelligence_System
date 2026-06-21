import streamlit as st
import joblib

@st.cache_resource
def load_model():
    return joblib.load("models/churn_model.pkl")