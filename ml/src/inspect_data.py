import pandas as pd

DATA_PATH = "../data/creditcard.csv"

def main():
    df = pd.read_csv(DATA_PATH)

    print("\nDataset shape:")
    print(df.shape)

    print("\nFirst 5 rows:")
    print(df.head())

    print("\nColumn names:")
    print(df.columns.tolist())

    print("\nMissing values:")
    print(df.isnull().sum())

    print("\nClass distribution:")
    print(df["Class"].value_counts())

    print("\nClass distribution percentage:")
    print(df["Class"].value_counts(normalize=True) * 100)

    print("\nBasic stats:")
    print(df.describe())

if __name__ == "__main__":
    main()