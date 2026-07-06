def get_high_risk_transactions(report_df):
    return report_df[
        report_df["risk_label"] == "High Risk"
    ].to_dict(orient="records")


def get_suspicious_transactions(report_df):
    return report_df[
        report_df["risk_label"] == "Suspicious"
    ].to_dict(orient="records")


def get_all_transactions(report_df):
    return report_df.to_dict(orient="records")