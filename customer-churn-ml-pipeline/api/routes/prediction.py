# Import required libraries
import pandas as pd

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from api.database import get_db
from api.models import Prediction
from api.schemas import CustomerFeatures, PredictionResponse

# Create API router
router = APIRouter()


# Customer churn prediction endpoint
@router.post("/predict", response_model=PredictionResponse)
def predict_churn(
    payload: CustomerFeatures,
    request: Request,
    db: Session = Depends(get_db)
):

    # Load trained ML model
    model = request.app.state.model

    if model is None:
        raise HTTPException(
            status_code=503,
            detail="Model not loaded. Train the model first."
        )

    try:
        # Convert customer input into dictionary
        customer_data = payload.model_dump()

        # Extract optional customer ID
        customer_id = customer_data.pop("customerID", None)

        # Convert dictionary into a 2D Pandas DataFrame
        input_df = pd.DataFrame([customer_data])

        # Generate churn probability
        probabilities = model.predict_proba(input_df)

        probability = float(probabilities[0][1])

        # Generate binary prediction
        prediction = int(probability >= 0.5)

        # Determine customer risk level
        if probability >= 0.70:
            risk = "High"

        elif probability >= 0.40:
            risk = "Medium"

        else:
            risk = "Low"

        # Create database prediction record
        record = Prediction(
            customer_id=customer_id,
            churn_probability=probability,
            churn_prediction=prediction,
            input_features=customer_data
        )

        # Save prediction to PostgreSQL
        db.add(record)
        db.commit()
        db.refresh(record)

        # Return prediction response
        return PredictionResponse(
            churn_prediction=prediction,
            churn_label="Churn" if prediction else "No Churn",
            churn_probability=round(probability, 4),
            risk_level=risk,
            prediction_id=record.id
        )

    except Exception as e:

        # Roll back database transaction if necessary
        db.rollback()

        # Return error details
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )