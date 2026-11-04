# Import libraries
import json

from api.database import SessionLocal
from api.models import Prediction

from src.config import REPORT_DIR


# Monitor stored predictions
def main():

    # Connect to database
    db = SessionLocal()

    try:

        # Retrieve recent predictions
        predictions = db.query(Prediction).order_by(
            Prediction.created_at.desc()
        ).limit(1000).all()

        total = len(predictions)

        # Calculate monitoring metrics
        summary = {
            "total_predictions": total,

            "high_risk_predictions": sum(
                p.churn_probability >= 0.7
                for p in predictions
            ),

            "average_churn_probability": (
                sum(p.churn_probability for p in predictions) / total
                if total else None
            )
        }

    finally:
        db.close()

    # Save monitoring report
    with open(
        REPORT_DIR / "monitoring_summary.json",
        "w"
    ) as file:

        json.dump(summary, file, indent=4)

    print(summary)


if __name__ == "__main__":
    main()