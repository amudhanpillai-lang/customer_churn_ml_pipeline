# Import libraries
import json
import pandas as pd
import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)

from src.config import DATA_PATH, MODEL_PATH, METADATA_PATH
from src.preprocessing import (
    clean_data,
    split_features_target,
    build_preprocessor
)


# Main training function
def main():

    # Load dataset
    df = pd.read_csv(DATA_PATH)

    # Clean dataset
    df = clean_data(df)

    # Separate features and target
    X, y = split_features_target(df)

    # Split training and testing data
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    # Create complete ML pipeline
    pipeline = Pipeline([
        ("preprocessor", build_preprocessor(X_train)),

        ("classifier", RandomForestClassifier(
            n_estimators=400,
            max_depth=12,
            class_weight="balanced",
            random_state=42,
            n_jobs=-1
        ))
    ])

    # Train model
    pipeline.fit(X_train, y_train)

    # Generate predictions
    predictions = pipeline.predict(X_test)

    # Calculate churn probabilities
    probabilities = pipeline.predict_proba(X_test)[:, 1]

    # Evaluate model
    metrics = {
        "accuracy": accuracy_score(y_test, predictions),
        "precision": precision_score(y_test, predictions),
        "recall": recall_score(y_test, predictions),
        "f1_score": f1_score(y_test, predictions),
        "roc_auc": roc_auc_score(y_test, probabilities)
    }

    # Display results
    print("\nModel Evaluation:")
    print(json.dumps(metrics, indent=4))

    # Save trained model
    joblib.dump(pipeline, MODEL_PATH)

    # Save model metadata
    metadata = {
        "model": "RandomForestClassifier",
        "features": X.columns.tolist(),
        "metrics": metrics
    }

    with open(METADATA_PATH, "w") as file:
        json.dump(metadata, file, indent=4)

    print("\nModel saved successfully!")


if __name__ == "__main__":
    main()
