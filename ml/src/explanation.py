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