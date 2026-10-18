
import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

loaded_model = joblib.load("customer_churn_pipeline.joblib")
app = FastAPI(title="Customer Churn Prediction API")

class CustomerData(BaseModel):
    Territory: str
    DeviceType: str
    Promotion: str
    HasRenewed: str
    PlanType: str
    BaseFee: float
    AdditionalFeatureSpend: float
    NumberOfPenalties: float
    CurrentPeriodUsage: float
    PriorPeriodUsage: float
    ServiceRating: float
    ServiceTickets: float
    StartMonth: str
    StartWeek: str
    CustomerTenure: float

@app.get("/")
def home():
    return {"message": "Customer Churn Prediction API is running"}

@app.post("/predict")
def predict_churn(customer: CustomerData):
    customer_df = pd.DataFrame([customer.model_dump()])
    prediction = int(loaded_model.predict(customer_df)[0])
    probability = float(loaded_model.predict_proba(customer_df)[0][1])

    return {
        "churn_prediction": "Yes" if prediction == 1 else "No",
        "churn_probability": round(probability, 4)
    }
