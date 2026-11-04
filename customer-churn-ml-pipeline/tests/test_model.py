# Import libraries
import pandas as pd

from src.preprocessing import (
    clean_data,
    split_features_target,
    build_preprocessor
)


# Test preprocessing functionality
def test_clean_data():

    # Create sample dataset
    df = pd.DataFrame({
        "customerID": ["1", "2"],
        "tenure": [10, 20],
        "TotalCharges": ["100", "200"],
        "Churn": ["Yes", "No"]
    })

    # Clean data
    cleaned = clean_data(df)

    # Separate features and target
    X, y = split_features_target(cleaned)

    # Verify results
    assert "customerID" not in X.columns
    assert y.tolist() == [1, 0]

    # Verify preprocessor
    assert build_preprocessor(X) is not None