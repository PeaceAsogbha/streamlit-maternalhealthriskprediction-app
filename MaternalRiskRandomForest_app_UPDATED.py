import streamlit as st
import pickle
import pandas as pd

# =========================
# LOAD MODEL
# =========================
with open('MaternalRisk_rf_model.pkl', 'rb') as f:
    model = pickle.load(f)

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Maternal Risk Predictor",
    layout="centered"
)

# =========================
# CENTERED ICON + TITLE
# =========================
st.markdown("<h1 style='text-align: center;'>🩺</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center;'>Maternal Risk Prediction System</h2>", unsafe_allow_html=True)

st.markdown("Enter patient health details to predict maternal risk level.")

st.divider()

# =========================
# INPUT SECTION (SINGLE COLUMN)
# =========================

st.subheader("Enter Patient Details")

age = st.number_input("Age (years)", 10, 60, 25)
systolic_bp = st.number_input("Systolic BP (mmHg)", 80, 200, 120)
diastolic_bp = st.number_input("Diastolic BP (mmHg)", 40, 120, 80)
heart_rate = st.number_input("Heart Rate (bpm)", 40, 150, 75)

bs = st.number_input("Blood Sugar (mmol/L)", 2.0, 20.0, 5.5)
body_temp_f = st.number_input("Body Temperature (°F)", 95.0, 110.0, 98.6)

st.divider()

# =========================
# DERIVED FEATURES (AUTO DISPLAY)
# =========================

# Convert Fahrenheit → Celsius
body_temp_c = (body_temp_f - 32) * (5/9)

pulse_pressure = systolic_bp - diastolic_bp
shock_index = heart_rate / systolic_bp if systolic_bp != 0 else 0
temp_deviation = body_temp_c - 37

# --- BS Risk ---
if bs < 6.7:
    bs_risk = 0
elif bs <= 11.1:
    bs_risk = 1
else:
    bs_risk = 2

# --- Age Group ---
if age < 20:
    age_group = 0
elif age <= 35:
    age_group = 1
else:
    age_group = 2

# --- BP Category ---
if systolic_bp < 120 and diastolic_bp < 80:
    bp_category = 0
elif systolic_bp < 140:
    bp_category = 1
else:
    bp_category = 2

# =========================
# DISPLAY DERIVED VALUES
# =========================

st.subheader("Derived Health Indicators")

st.write(f"Pulse Pressure (mmHg): {pulse_pressure}")
st.write(f"Shock Index: {shock_index:.2f}")

st.divider()

# =========================
# PREDICTION
# =========================
if st.button("🔍 Predict Risk Level"):

    input_df = pd.DataFrame([{
        'Age': age,
        'SystolicBP': systolic_bp,
        'DiastolicBP': diastolic_bp,
        'BS': bs,
        'BodyTemp': body_temp_f,  # IMPORTANT: keep original unit as trained
        'HeartRate': heart_rate,
        'Pulse_Pressure': pulse_pressure,
        'Shock_Index': shock_index,
        'Temp_Deviation': temp_deviation,
        'BS_Risk': bs_risk,
        'Age_Group': age_group,
        'BP_Category': bp_category
    }])

    prediction = model.predict(input_df)[0]

    # =========================
    # OUTPUT + HEALTH MESSAGE
    # =========================
    if prediction == 0:
        st.success("🟢 Low Risk")
        st.info("Your physiological indicators suggest that the pregnancy is healthy with minimal health concerns for both the mother and baby.")

    elif prediction == 1:
        st.warning("🟡 Medium Risk")
        st.info("Your physiological indicators suggest that there might be some mild complications in the pregnancy that should be monitored closely.")

    else:
        st.error("🔴 High Risk")
        st.info("Your physiological indicators suggest significant health concerns that could lead to complications for the mother or baby, requiring close monitoring and medical intervention.")