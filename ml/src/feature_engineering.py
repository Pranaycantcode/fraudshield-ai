import pandas as pd


def engineer_transaction_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["hour"] = df["timestamp"].dt.hour

    user_avg_amount = df.groupby("user_id")["amount"].transform("mean")
    user_txn_count = df.groupby("user_id")["transaction_id"].transform("count")

    df["amount_to_user_avg_ratio"] = df["amount"] / user_avg_amount
    df["is_unusual_hour"] = df["hour"].apply(lambda hour: 1 if hour < 6 or hour > 23 else 0)

    df["user_transaction_count"] = user_txn_count

    df["is_new_location"] = (
        df.groupby("user_id")["location"]
        .transform(lambda locations: locations != locations.mode()[0])
        .astype(int)
    )

    df["is_new_device"] = (
        df.groupby("user_id")["device_id"]
        .transform(lambda devices: devices != devices.mode()[0])
        .astype(int)
    )

    df["is_unknown_merchant"] = df["merchant"].str.lower().str.contains("unknown").astype(int)

    return df