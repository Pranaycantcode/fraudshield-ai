import sys
from pathlib import Path
import pandas as pd


from fastapi import UploadFile
from fastapi import HTTPException


ML_SRC_PATH = Path(__file__).resolve().parents[1] / "ml" / "src"
sys.path.append(str(ML_SRC_PATH))

from feature_engineering import engineer_transaction_features
from risk_scoring import calculate_risk_score, get_risk_label
from explanation import generate_explanation
from analytics import generate_dashboard_analytics, generate_summary
from report import get_high_risk_transactions, get_all_transactions


REQUIRED_COLUMNS = {
    "transaction_id",
    "user_id",
    "timestamp",
    "amount",
    "merchant",
    "category",
    "location",
    "device_id",
    "transaction_type",
}

def validate_transaction_csv(df: pd.DataFrame):
    missing_columns = REQUIRED_COLUMNS - set(df.columns)

    if missing_columns:
        raise HTTPException(
            status_code=400,
            detail=f"Missing required columns: {', '.join(sorted(missing_columns))}",
        )

    if df.empty:
        raise HTTPException(
            status_code=400,
            detail="Uploaded CSV is empty.",
        )

    try:
        pd.to_datetime(df["timestamp"])
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid timestamp format. Use YYYY-MM-DD HH:MM:SS.",
        )

    if not pd.api.types.is_numeric_dtype(df["amount"]):
        raise HTTPException(
            status_code=400,
            detail="Amount column must contain numeric values.",
        )


async def process_transaction_csv(file: UploadFile):
    df = pd.read_csv(file.file)
    
    validate_transaction_csv(df)

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
    
    risk_distribution = report_df["risk_label"].value_counts().to_dict()

    summary = generate_summary(report_df)
    analytics = generate_dashboard_analytics(report_df)

    return {
    "summary": summary,
    "analytics": analytics,
    "high_risk_transactions": get_high_risk_transactions(report_df),
    "transactions": get_all_transactions(report_df),
}