import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "WA_Fn-UseC_-Telco-Customer-Churn.csv"

# Load dataset
df = pd.read_csv(DATA_PATH)

print(df.head())
print(df.shape)

# Check missing values
print(df.isnull().sum())

# Convert TotalCharges to numeric
df["TotalCharges"] = pd.to_numeric(
    df["TotalCharges"], errors="coerce"
)

# Remove missing values
df.dropna(inplace=True)

# Save cleaned dataset
df.to_csv(DATA_PATH.parent / "telco_eda_clean.csv", index=False)

print("Cleaned dataset saved successfully!")
print("Final shape:", df.shape)