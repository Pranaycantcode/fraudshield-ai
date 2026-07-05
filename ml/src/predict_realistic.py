import pandas as pd

from feature_engineering import engineer_transaction_features
from risk_scoring import calculate_risk_score, get_risk_label
from explanation import generate_explanation


INPUT_PATH = "../data/sample/transactions_sample.csv"
OUTPUT_PATH = "../data/sample/fraud_report_sample.csv"



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