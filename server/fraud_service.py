import sys
from pathlib import Path
import pandas as pd

from fastapi import UploadFile

ML_SRC_PATH = Path(__file__).resolve().parents[1] / "ml" / "src"
sys.path.append(str(ML_SRC_PATH))

from feature_engineering import engineer_transaction_features
from risk_scoring import calculate_risk_score, get_risk_label


async def process_transaction_csv(file: UploadFile):
    df = pd.read_csv(file.file)

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

    return {
        "total_transactions": len(report_df),
        "high_risk_count": int((report_df["risk_label"] == "High Risk").sum()),
        "suspicious_count": int((report_df["risk_label"] == "Suspicious").sum()),
        "safe_count": int((report_df["risk_label"] == "Safe").sum()),
        "transactions": report_df.to_dict(orient="records"),
    }


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