from pathlib import Path
import streamlit as st
import joblib

@st.cache_resource
def load_model():

    project_root = Path(__file__).resolve().parent.parent

    model_path = project_root / "models" / "churn_model.pkl"

    return joblib.load(model_path)