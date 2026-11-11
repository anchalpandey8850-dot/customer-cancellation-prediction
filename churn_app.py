

import streamlit as st
import pandas as pd
import requests

# ==================================================
# STEP 1: PAGE CONFIGURATION
# ==================================================
st.set_page_config(
    page_title="Customer Cancellation Prediction",
    page_icon="📊",
    layout="wide"
)

# ==================================================
# STEP 2: FASTAPI BACKEND URL
# ==================================================
API_BASE_URL = "https://customer-cancellation-prediction-4.onrender.com"

# ==================================================
# STEP 3: DASHBOARD HEADER
# ==================================================
st.title("📊 Customer Cancellation Prediction Dashboard")

st.write(
    "Enter customer details to predict whether "
    "the customer is likely to cancel the service."
)

st.divider()

# ==================================================
# STEP 4: CHECK BACKEND CONNECTION
# ==================================================
st.subheader("Backend Status")

try:
    health_response = requests.get(
        f"{API_BASE_URL}/",
        timeout=60
    )

    health_response.raise_for_status()

    health_data = health_response.json()

    st.success("FastAPI backend is connected and running.")

    st.write("Backend Response:", health_data)

except requests.exceptions.RequestException as error:
    st.error("Unable to connect to FastAPI backend.")
    st.exception(error)

except ValueError:
    st.error("Backend did not return valid JSON.")

st.divider()

# ==================================================
# STEP 5: CUSTOMER DETAILS FORM
# ==================================================
st.subheader("Enter Customer Details")

with st.form("customer_form"):

    col1, col2 = st.columns(2)

    with col1:
        Territory = st.text_input(
            "Territory",
            value="North"
        )

        DeviceType = st.text_input(
            "Device Type",
            value="iPhone"
        )

        Promotion = st.selectbox(
            "Promotion",
            options=["no", "yes"]
        )

        HasRenewed = st.selectbox(
            "Has Renewed",
            options=["no", "yes"]
        )

        PlanType = st.text_input(
            "Plan Type",
            value="Red Plan"
        )

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
            "Number Of Penalties",
            min_value=0.0,
            value=0.0
        )

    with col2:
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
            value=0.0
        )

        StartMonth = st.text_input(
            "Start Month",
            value="Jan"
        )

        StartWeek = st.text_input(
            "Start Week",
            value="Week 1"
        )

        CustomerTenure = st.number_input(
            "Customer Tenure",
            min_value=0.0,
            value=12.0
        )

    submitted = st.form_submit_button(
        "Predict Cancellation",
        type="primary",
        use_container_width=True
    )

# ==================================================
# STEP 6: SEND CUSTOMER DATA TO FASTAPI
# ==================================================
if submitted:

    customer_data = {
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
    }

    try:
        with st.spinner(
            "Sending customer details to FastAPI..."
        ):

            response = requests.post(
                f"{API_BASE_URL}/predict",
                json=customer_data,
                timeout=120
            )

            response.raise_for_status()

            result = response.json()

        # ==================================================
        # STEP 7: VALIDATE API RESPONSE
        # ==================================================
        required_keys = {
            "churn_prediction",
            "churn_probability"
        }

        missing_keys = required_keys - set(result.keys())

        if missing_keys:
            raise ValueError(
                f"Missing API response fields: {missing_keys}"
            )

        prediction = result["churn_prediction"]
        probability = float(result["churn_probability"])

        if prediction not in ["Yes", "No"]:
            raise ValueError("Invalid cancellation prediction.")

        if not 0 <= probability <= 1:
            raise ValueError("Invalid cancellation probability.")

        # ==================================================
        # STEP 8: DISPLAY PREDICTION RESULT
        # ==================================================
        st.divider()
        st.subheader("Customer Cancellation Prediction")

        if prediction == "Yes":
            st.error(
                "Prediction: Customer is likely to cancel."
            )
        else:
            st.success(
                "Prediction: Customer is unlikely to cancel."
            )

        metric1, metric2 = st.columns(2)

        metric1.metric(
            "Cancellation Prediction",
            prediction
        )

        metric2.metric(
            "Cancellation Probability",
            f"{probability:.1%}"
        )

    # ==================================================
    # STEP 9: ERROR HANDLING
    # ==================================================
    except requests.exceptions.HTTPError as error:

        try:
            details = response.json().get(
                "detail",
                response.text
            )
        except Exception:
            details = response.text

        st.error(f"FastAPI returned an error: {details}")

    except requests.exceptions.Timeout:
        st.error(
            "Request timed out. Render may be waking up. "
            "Please try again."
        )

    except requests.exceptions.RequestException as error:
        st.error(f"Unable to reach FastAPI: {error}")

    except (ValueError, KeyError, TypeError) as error:
        st.error(f"Unable to process prediction response: {error}")

    except Exception as error:
        st.error("An unexpected error occurred.")
        st.exception(error)
