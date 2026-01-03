import streamlit as st
import pandas as pd
import numpy as np
from datetime import date

# -------------------------------
# Silent Dropout Score Function
# -------------------------------
def predict_risk(X):
    # Normalize inputs (capped)
    days_contact = np.clip(X["Days_Since_Last_Contact"], 0, 60)
    refill_delay = np.clip(X["Medicine_Refill_Delay_days"], 0, 60)
    missed_labs = np.clip(X["Missed_Lab_Tests"], 0, 10)
    late_followup = np.clip(X["Days_Late_Follow_Up"], 0, 30)
    expected_gap = np.clip(X["Expected_Gap_Between_Visits_days"], 0, 60)

    # Weighted Silent Dropout Score
    silent_score = (
        (days_contact * 0.30) +
        (refill_delay * 0.30) +
        (missed_labs * 5 * 0.20) +
        (late_followup * 0.15) +
        (expected_gap * 0.05)
    )

    silent_score = np.clip(silent_score, 0, 100)

    # Risk Classification
    risk = np.where(
        silent_score > 60, "HIGH",
        np.where(silent_score > 30, "MEDIUM", "LOW")
    )

    return silent_score, risk

# -------------------------------
# Streamlit UI
# -------------------------------
st.set_page_config(page_title="Patient Silent Dropout Predictor", layout="centered")

st.title("🩺 Patient Silent Dropout Risk Predictor")
st.markdown("Predict dropout risk using behavioral inactivity patterns.")

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
    st.metric("Silent Dropout Score", round(float(silent_score[0]), 2))
    st.metric("Risk Level", risk_level[0])

    if risk_level[0] == "HIGH":
        st.error("🚨 Immediate intervention required!")
    elif risk_level[0] == "MEDIUM":
        st.warning("⚠️ Monitor patient closely.")
    else:
        st.success("✅ Patient engagement is healthy.")

