# Import libraries
import pandas as pd
import joblib
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay
)

from src.config import DATA_PATH, MODEL_PATH, REPORT_DIR
from src.preprocessing import clean_data, split_features_target


def main():

    # Load and clean dataset
    df = clean_data(pd.read_csv(DATA_PATH))

    # Separate features and target
    X, y = split_features_target(df)

    # Reproduce test split used during training
    _, X_test, _, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    # Load trained model
    model = joblib.load(MODEL_PATH)

    # Predict test data
    predictions = model.predict(X_test)

    # Print classification report
    print(classification_report(y_test, predictions))

    # Generate confusion matrix
    cm = confusion_matrix(y_test, predictions)

    # Visualize confusion matrix
    display = ConfusionMatrixDisplay(
        confusion_matrix=cm,
        display_labels=["No Churn", "Churn"]
    )

    display.plot()

    plt.tight_layout()
    plt.savefig(REPORT_DIR / "confusion_matrix.png")
    plt.close()


if __name__ == "__main__":
    main()