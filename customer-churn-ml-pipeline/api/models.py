# Import libraries
from datetime import datetime

from sqlalchemy import (
    Integer,
    Float,
    String,
    JSON,
    DateTime
)

from sqlalchemy.orm import Mapped, mapped_column

from api.database import Base


# Database table for prediction history
class Prediction(Base):

    __tablename__ = "predictions"

    # Unique prediction ID
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    # Customer ID
    customer_id: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    # Predicted churn probability
    churn_probability: Mapped[float] = mapped_column(
        Float
    )

    # Predicted churn class
    churn_prediction: Mapped[int] = mapped_column(
        Integer
    )

    # Store input features
    input_features: Mapped[dict] = mapped_column(JSON)

    # Prediction timestamp
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )