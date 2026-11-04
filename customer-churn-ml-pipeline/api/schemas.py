# Import Pydantic
from pydantic import BaseModel, Field, ConfigDict


# Input schema for customer information
class CustomerFeatures(BaseModel):

    model_config = ConfigDict(extra="allow")

    gender: str
    SeniorCitizen: int = Field(ge=0, le=1)
    Partner: str
    Dependents: str
    tenure: int = Field(ge=0)

    PhoneService: str
    MultipleLines: str
    InternetService: str
    OnlineSecurity: str
    OnlineBackup: str
    DeviceProtection: str
    TechSupport: str
    StreamingTV: str
    StreamingMovies: str

    Contract: str
    PaperlessBilling: str
    PaymentMethod: str

    MonthlyCharges: float = Field(ge=0)
    TotalCharges: float = Field(ge=0)


# Output schema
class PredictionResponse(BaseModel):

    churn_prediction: int
    churn_label: str
    churn_probability: float
    risk_level: str
    prediction_id: int | None = None