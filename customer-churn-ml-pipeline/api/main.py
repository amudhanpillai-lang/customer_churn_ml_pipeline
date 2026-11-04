# Import libraries
from contextlib import asynccontextmanager

import joblib
from fastapi import FastAPI

from api.database import Base, engine
from api import models

from api.routes import prediction, analytics

from src.config import MODEL_PATH


# Application startup and shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):

    # Create database tables
    Base.metadata.create_all(bind=engine)

    # Load trained model
    if MODEL_PATH.exists():
        app.state.model = joblib.load(MODEL_PATH)
    else:
        app.state.model = None

    yield


# Initialize FastAPI
app = FastAPI(
    title="Customer Churn Prediction API",
    description="Predict customer churn using Machine Learning",
    version="1.0",
    lifespan=lifespan
)


# Register API routes
app.include_router(
    prediction.router,
    prefix="/api",
    tags=["Prediction"]
)

app.include_router(
    analytics.router,
    prefix="/api",
    tags=["Analytics"]
)


# Health check endpoint
@app.get("/health")
def health():

    return {
        "status": "ok",
        "model_loaded": app.state.model is not None
    }