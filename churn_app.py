
streamlit_code = '''
import streamlit as st
import pandas as pd
import joblib
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Customer Cancellation Prediction",
    page_icon="📊",
    layout="centered"
)

# Load trained model
MODEL_PATH = Path(__file__).parent / "customer_churn_pipeline.joblib"

@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)

try:
    model = load_model()
except Exception as e:
    st.error(f"Could not load the trained model: {e}")
    st.stop()

# App title
st.title("Customer Cancellation Prediction")
st.write(
    "Enter customer details below to estimate the likelihood "
    "of customer cancellation."
)

st.info("Fill in the customer information and click Predict Cancellation.")

# Customer input form
with st.form("customer_form"):

    st.subheader("Customer Information")

    Territory = st.text_input("Territory", "North")
    DeviceType = st.text_input("Device Type", "iPhone")

    Promotion = st.selectbox(
        "Promotion",
        ["no", "yes"]
    )

    HasRenewed = st.selectbox(
        "Has Renewed",
        ["no", "yes"]
    )

    PlanType = st.text_input("Plan Type", "Red Plan")

    st.subheader("Usage and Account Details")

    BaseFee = st.number_input(
        "Base Fee",
        min_value=0.0,
        value=50.0
    )

    AdditionalFeatureSpend = st.number_input(
        "Additional Feature Spend",
        min_value=0.0,
        value=10.0
    )

    NumberOfPenalties = st.number_input(
        "Number of Penalties",
        min_value=0.0,
        value=0.0,
        step=1.0
    )

    CurrentPeriodUsage = st.number_input(
        "Current Period Usage",
        min_value=0.0,
        value=100.0
    )

    PriorPeriodUsage = st.number_input(
        "Prior Period Usage",
        min_value=0.0,
        value=100.0
    )

    ServiceRating = st.number_input(
        "Service Rating",
        min_value=0.0,
        value=4.0
    )

    ServiceTickets = st.number_input(
        "Service Tickets",
        min_value=0.0,
        value=0.0,
        step=1.0
    )

    st.subheader("Customer Tenure")

    StartMonth = st.text_input("Start Month", "Jan")
    StartWeek = st.text_input("Start Week", "Week 1")

    CustomerTenure = st.number_input(
        "Customer Tenure",
        min_value=0.0,
        value=12.0
    )

    submitted = st.form_submit_button("Predict Cancellation")

# Prediction
if submitted:

    customer = pd.DataFrame([{
        "Territory": Territory,
        "DeviceType": DeviceType,
        "Promotion": Promotion,
        "HasRenewed": HasRenewed,
        "PlanType": PlanType,
        "BaseFee": BaseFee,
        "AdditionalFeatureSpend": AdditionalFeatureSpend,
        "NumberOfPenalties": NumberOfPenalties,
        "CurrentPeriodUsage": CurrentPeriodUsage,
        "PriorPeriodUsage": PriorPeriodUsage,
        "ServiceRating": ServiceRating,
        "ServiceTickets": ServiceTickets,
        "StartMonth": StartMonth,
        "StartWeek": StartWeek,
        "CustomerTenure": CustomerTenure
    }])

    try:
        prediction = int(model.predict(customer)[0])
        probability = float(model.predict_proba(customer)[0][1])

        st.subheader("Prediction Result")

        if prediction == 1:
            st.error("Prediction: Customer is likely to cancel.")
        else:
            st.success("Prediction: Customer is unlikely to cancel.")

        st.metric(
            label="Estimated Cancellation Probability",
            value=f"{probability:.1%}"
        )

        st.caption(
            "This is a machine-learning estimate, not a guarantee "
            "of future customer behavior."
        )

    except Exception as e:
        st.error(f"Prediction failed: {e}")
'''

with open("churn_app.py", "w", encoding="utf-8") as file:
    file.write(streamlit_code)

print("churn_app.py updated successfully!")
