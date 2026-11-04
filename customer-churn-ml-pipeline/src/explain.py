# Import libraries
import pandas as pd
import joblib
import shap
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split

from src.config import DATA_PATH, MODEL_PATH, REPORT_DIR
from src.preprocessing import clean_data, split_features_target


def main():

    # Load dataset
    df = clean_data(pd.read_csv(DATA_PATH))

    # Separate features and target
    X, y = split_features_target(df)

    # Split dataset
    X_train, X_test, _, _ = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    # Load trained pipeline
    pipeline = joblib.load(MODEL_PATH)

    # Extract preprocessing and classifier
    preprocessor = pipeline.named_steps["preprocessor"]
    classifier = pipeline.named_steps["classifier"]

    # Select sample records
    sample = X_test.sample(
        min(200, len(X_test)),
        random_state=42
    )

    # Transform data
    transformed = preprocessor.transform(sample)

    # Get feature names
    feature_names = preprocessor.get_feature_names_out()

    # Create SHAP explainer
    explainer = shap.TreeExplainer(classifier)

    # Calculate SHAP values
    shap_values = explainer.shap_values(transformed)

    # Handle binary classification output
    if isinstance(shap_values, list):
        shap_values = shap_values[1]
    elif getattr(shap_values, "ndim", 0) == 3:
        shap_values = shap_values[:, :, 1]

    # Generate SHAP summary plot
    shap.summary_plot(
        shap_values,
        transformed,
        feature_names=feature_names,
        show=False
    )

    # Save visualization
    plt.savefig(
        REPORT_DIR / "shap_summary.png",
        bbox_inches="tight"
    )

    plt.close()

    print("SHAP explanation completed.")


if __name__ == "__main__":
    main()