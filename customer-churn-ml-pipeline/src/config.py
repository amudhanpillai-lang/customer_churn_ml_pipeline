# Import required libraries
from pathlib import Path
import os
from dotenv import load_dotenv

# Set project root directory
ROOT_DIR = Path(__file__).resolve().parents[1]

# Load environment variables
load_dotenv(ROOT_DIR / ".env")

# Define project paths
DATA_PATH = Path(os.getenv(
    "DATA_PATH",
    ROOT_DIR / "data/WA_Fn-UseC_-Telco-Customer-Churn.csv"
))

MODEL_DIR = ROOT_DIR / "models"
REPORT_DIR = ROOT_DIR / "reports"

MODEL_PATH = Path(os.getenv(
    "MODEL_PATH", MODEL_DIR / "churn_pipeline.joblib"
))

METADATA_PATH = Path(os.getenv(
    "METADATA_PATH", MODEL_DIR / "model_metadata.json"
))

# Create folders if they don't exist
MODEL_DIR.mkdir(exist_ok=True)
REPORT_DIR.mkdir(exist_ok=True)