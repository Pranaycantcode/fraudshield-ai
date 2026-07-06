def generate_dashboard_analytics(report_df):
    risk_distribution = report_df["risk_label"].value_counts().to_dict()

    category_risk = (
        report_df.groupby("category")["risk_score"]
        .mean()
        .sort_values(ascending=False)
        .round(3)
        .to_dict()
    )

    location_risk = (
        report_df.groupby("location")["risk_score"]
        .mean()
        .sort_values(ascending=False)
        .round(3)
        .to_dict()
    )

    return {
        "risk_distribution": risk_distribution,
        "category_risk": category_risk,
        "location_risk": location_risk,
    }


def generate_summary(report_df):
    total = len(report_df)
    high_risk_count = int((report_df["risk_label"] == "High Risk").sum())
    suspicious_count = int((report_df["risk_label"] == "Suspicious").sum())
    safe_count = int((report_df["risk_label"] == "Safe").sum())

    fraud_risk_percentage = round(
        ((high_risk_count + suspicious_count) / total) * 100,
        2,
    )

    return {
        "total_transactions": total,
        "high_risk_count": high_risk_count,
        "suspicious_count": suspicious_count,
        "safe_count": safe_count,
        "fraud_risk_percentage": fraud_risk_percentage,
    }