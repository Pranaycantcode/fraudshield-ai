import pandas as pd

from feature_engineering import engineer_transaction_features
from risk_scoring import calculate_risk_score, get_risk_label


INPUT_PATH = "../data/sample/transactions_sample.csv"
OUTPUT_PATH = "../data/sample/fraud_report_sample.csv"


def generate_explanation(row) -> str:
    reasons = []

    if row["amount_to_user_avg_ratio"] >= 3:
        reasons.append(
            f"amount is {row['amount_to_user_avg_ratio']:.1f}x higher than this user's average"
        )

    if row["is_unusual_hour"] == 1:
        reasons.append("transaction happened at an unusual hour")

    if row["is_new_location"] == 1:
        reasons.append("location differs from the user's usual location")

    if row["is_new_device"] == 1:
        reasons.append("device differs from the user's usual device")

    if row["is_unknown_merchant"] == 1:
        reasons.append("merchant appears unfamiliar or unknown")

    if not reasons:
        return "No major risk factors detected."

    return "; ".join(reasons)


def main():
    df = pd.read_csv(INPUT_PATH)

    engineered_df = engineer_transaction_features(df)

    engineered_df["risk_score"] = engineered_df.apply(calculate_risk_score, axis=1)
    engineered_df["risk_label"] = engineered_df["risk_score"].apply(get_risk_label)
    engineered_df["explanation"] = engineered_df.apply(generate_explanation, axis=1)

    report_columns = [
        "transaction_id",
        "user_id",
        "timestamp",
        "amount",
        "merchant",
        "category",
        "location",
        "device_id",
        "transaction_type",
        "risk_score",
        "risk_label",
        "explanation",
    ]

    report_df = engineered_df[report_columns]

    print(report_df)

    report_df.to_csv(OUTPUT_PATH, index=False)
    print(f"\nFraud report saved to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()