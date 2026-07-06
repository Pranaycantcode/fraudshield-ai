def assign_synthetic_label(row) -> int:
    risk_signals = 0

    if row["amount_to_user_avg_ratio"] >= 3:
        risk_signals += 1

    if row["is_unusual_hour"] == 1:
        risk_signals += 1

    if row["is_new_location"] == 1:
        risk_signals += 1

    if row["is_new_device"] == 1:
        risk_signals += 1

    if row["is_unknown_merchant"] == 1:
        risk_signals += 1

    return 1 if risk_signals >= 2 else 0