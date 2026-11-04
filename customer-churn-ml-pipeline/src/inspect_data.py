# Import pandas
import pandas as pd
from src.config import DATA_PATH

# Main function
def main():

    # Load dataset
    df = pd.read_csv(DATA_PATH)

    # Display dataset information
    print("Dataset Shape:", df.shape)

    print("\nColumn Names:")
    print(df.columns.tolist())

    print("\nData Types:")
    print(df.dtypes)

    # Check missing values
    print("\nMissing Values:")
    print(df.isnull().sum())

    # Check duplicate records
    print("\nDuplicates:", df.duplicated().sum())

    # Display target distribution
    print("\nChurn Distribution:")
    print(df["Churn"].value_counts())

    # Display first five records
    print("\nFirst Five Rows:")
    print(df.head())


if __name__ == "__main__":
    main()