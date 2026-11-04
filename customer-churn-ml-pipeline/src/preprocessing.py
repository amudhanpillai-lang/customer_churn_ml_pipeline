# Import required libraries
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# Define target column
TARGET = "Churn"

# Columns to remove
DROP_COLUMNS = ["customerID"]


# Clean dataset
def clean_data(df):

    # Create a copy
    df = df.copy()

    # Convert TotalCharges into numeric
    df["TotalCharges"] = pd.to_numeric(
        df["TotalCharges"], errors="coerce"
    )

    # Remove duplicate records
    df = df.drop_duplicates()

    # Convert target labels into binary values
    df[TARGET] = df[TARGET].map({
        "Yes": 1,
        "No": 0
    })

    # Remove rows with missing target
    df = df.dropna(subset=[TARGET])

    return df


# Separate features and target
def split_features_target(df):

    y = df[TARGET].astype(int)

    X = df.drop(
        columns=[TARGET] + [
            col for col in DROP_COLUMNS if col in df.columns
        ]
    )

    return X, y


# Build preprocessing pipeline
def build_preprocessor(X):

    # Identify numerical columns
    numerical_features = X.select_dtypes(
        include=["number"]
    ).columns.tolist()

    # Identify categorical columns
    categorical_features = X.select_dtypes(
        exclude=["number"]
    ).columns.tolist()

    # Numerical preprocessing
    numerical_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ])

    # Categorical preprocessing
    categorical_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore"))
    ])

    # Combine both pipelines
    preprocessor = ColumnTransformer([
        ("numerical", numerical_pipeline, numerical_features),
        ("categorical", categorical_pipeline, categorical_features)
    ])

    return preprocessor