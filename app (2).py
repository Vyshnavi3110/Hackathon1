import streamlit as st
import pandas as pd
import numpy as np
from datetime import date

# -------------------------------
# Dummy model (for demo)
# -------------------------------
def predict_risk(X):
    silent_score = np.clip(
        X["Medicine_Refill_Delay_days"] * 0.5 +
        X["Days_Since_Last_Contact"] * 0.3,
        0, 100
    )

    risk = np.where(
        silent_score > 60, "High",
        np.where(silent_score > 30, "Medium", "Low")
    )

    return silent_score, risk

# -------------------------------
# Streamlit UI
# -------------------------------
st.set_page_config(page_title="Patient Dropout Risk Predictor", layout="centered")

st.title("🩺 Patient Silent Dropout Risk Predictor")
st.markdown("Enter patient follow-up details to predict dropout risk.")

# Inputs
last_follow_up = st.date_input("Last Follow-Up Date", value=date.today())

expected_gap = st.number_input("Expected Gap Between Visits (days)", min_value=0)
refill_delay = st.number_input("Medicine Refill Delay (days)", min_value=0)
days_since_contact = st.number_input("Days Since Last Contact", min_value=0)
missed_labs = st.number_input("Missed Lab Tests", min_value=0)
days_late_followup = st.number_input("Days Late for Follow-Up", min_value=0)

# Prediction
if st.button("🔍 Predict Risk"):
    input_df = pd.DataFrame({
        "Expected_Gap_Between_Visits_days": [expected_gap],
        "Medicine_Refill_Delay_days": [refill_delay],
        "Days_Since_Last_Contact": [days_since_contact],
        "Missed_Lab_Tests": [missed_labs],
        "Days_Late_Follow_Up": [days_late_followup]
    })

    silent_score, risk_level = predict_risk(input_df)

    st.success("Prediction Complete ✅")
    st.metric("Silent Dropout Score", round(float(silent_score.iloc[0]), 2))
    st.metric("Risk Level", risk_level[0])
