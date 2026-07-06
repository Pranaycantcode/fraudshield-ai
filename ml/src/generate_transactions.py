import random
from datetime import datetime, timedelta

import pandas as pd


USER_PROFILE_PATH = "../data/processed/user_profiles.csv"
OUTPUT_PATH = "../data/processed/synthetic_transactions.csv"

LOCATIONS = [
    "Mumbai",
    "Delhi",
    "Bangalore",
    "Pune",
    "Hyderabad",
    "Chennai",
    "Kolkata",
    "Ahmedabad",
    "Dubai",
    "Singapore",
]

MERCHANTS = {
    "Food": ["Swiggy", "Zomato", "Starbucks", "McDonalds"],
    "Shopping": ["Amazon", "Flipkart", "Myntra", "Unknown Electronics"],
    "Travel": ["Uber", "Ola", "MakeMyTrip", "IRCTC"],
    "Finance": ["Groww", "Zerodha", "Crypto Exchange"],
    "Entertainment": ["Netflix", "BookMyShow", "Spotify"],
}

TRANSACTION_TYPES = ["UPI", "Card", "NetBanking", "Wallet"]


def generate_transactions(num_transactions: int = 50000, fraud_rate: float = 0.015):
    users = pd.read_csv(USER_PROFILE_PATH)
    transactions = []

    for i in range(1, num_transactions + 1):
        user = users.sample(1).iloc[0]

        is_fraud = random.random() < fraud_rate

        category = random.choice(list(MERCHANTS.keys()))
        merchant = random.choice(MERCHANTS[category])

        amount = round(
            max(
                10,
                random.gauss(
                    user["average_transaction_amount"],
                    user["transaction_amount_std_dev"],
                ),
            ),
            2,
        )

        location = user["home_location"]
        device_id = random.choice(str(user["known_devices"]).split("|"))
        transaction_type = user["preferred_payment_type"]

        start_hour = int(user["active_start_hour"])
        end_hour = int(user["active_end_hour"])
        hour = random.randint(start_hour, end_hour)

        fraud_signals = []

        if is_fraud:
            fraud_type_count = random.randint(2, 4)

            possible_fraud_signals = [
                "high_amount",
                "new_location",
                "new_device",
                "unusual_hour",
                "unknown_merchant",
            ]

            selected_signals = random.sample(
                possible_fraud_signals,
                k=fraud_type_count,
            )

            if "high_amount" in selected_signals:
                amount = round(user["average_transaction_amount"] * random.uniform(4, 10), 2)
                fraud_signals.append("high_amount")

            if "new_location" in selected_signals:
                location = random.choice(
                    [loc for loc in LOCATIONS if loc != user["home_location"]]
                )
                fraud_signals.append("new_location")

            if "new_device" in selected_signals:
                device_id = f"UNKNOWN-{random.randint(10000, 99999)}"
                fraud_signals.append("new_device")

            if "unusual_hour" in selected_signals:
                hour = random.choice([0, 1, 2, 3, 4, 5])
                fraud_signals.append("unusual_hour")

            if "unknown_merchant" in selected_signals:
                category = random.choice(["Shopping", "Finance"])
                merchant = random.choice(["Unknown Electronics", "Crypto Exchange"])
                fraud_signals.append("unknown_merchant")

        timestamp = datetime(2026, 1, 1) + timedelta(
            days=random.randint(0, 364),
            hours=hour,
            minutes=random.randint(0, 59),
            seconds=random.randint(0, 59),
        )

        transactions.append(
            {
                "transaction_id": f"TXN{i:07d}",
                "user_id": user["user_id"],
                "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "amount": amount,
                "merchant": merchant,
                "category": category,
                "location": location,
                "device_id": device_id,
                "transaction_type": transaction_type,
                "fraud": int(is_fraud),
                "fraud_signals": "|".join(fraud_signals) if fraud_signals else "none",
            }
        )

    return pd.DataFrame(transactions)


def main():
    df = generate_transactions()

    df.to_csv(OUTPUT_PATH, index=False)

    print(f"Generated {len(df)} synthetic transactions")
    print(f"Saved to {OUTPUT_PATH}")
    print("\nFraud distribution:")
    print(df["fraud"].value_counts())
    print("\nFraud distribution percentage:")
    print(df["fraud"].value_counts(normalize=True) * 100)


if __name__ == "__main__":
    main()