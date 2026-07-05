def calculate_risk_score(row) -> float:
    score = 0

    if row["amount_to_user_avg_ratio"] >= 3:
        score += 0.30

    if row["is_unusual_hour"] == 1:
        score += 0.20

    if row["is_new_location"] == 1:
        score += 0.20

    if row["is_new_device"] == 1:
        score += 0.20

    if row["is_unknown_merchant"] == 1:
        score += 0.10

    return min(score, 1.0)


def get_risk_label(score: float) -> str:
    if score >= 0.7:
        return "High Risk"
    elif score >= 0.4:
        return "Suspicious"
    return "Safe"