import pandas as pd


def load_creditcard_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


def time_based_split(df: pd.DataFrame, train_size: float = 0.8):
    split_index = int(len(df) * train_size)
    train_df = df.iloc[:split_index]
    test_df = df.iloc[split_index:]
    return train_df, test_df