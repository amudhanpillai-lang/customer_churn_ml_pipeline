# Import libraries
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from api.database import get_db
from api.models import Prediction

# Create router
router = APIRouter()


# Get prediction analytics
@router.get("/analytics")
def get_analytics(db: Session = Depends(get_db)):

    # Count total predictions
    total = db.query(
        func.count(Prediction.id)
    ).scalar() or 0

    # Count predicted churn customers
    churned = db.query(
        func.count(Prediction.id)
    ).filter(
        Prediction.churn_prediction == 1
    ).scalar() or 0

    # Calculate average churn probability
    average_probability = db.query(
        func.avg(Prediction.churn_probability)
    ).scalar()

    # Return analytics
    return {
        "total_predictions": total,
        "predicted_churn": churned,
        "predicted_no_churn": total - churned,
        "predicted_churn_rate": (
            round(churned / total, 4) if total else 0
        ),
        "average_churn_probability": (
            round(float(average_probability), 4)
            if average_probability is not None
            else None
        )
    }