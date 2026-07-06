import random
import pandas as pd


LOCATIONS = [
    "Mumbai",
    "Delhi",
    "Bangalore",
    "Pune",
    "Hyderabad",
    "Chennai",
    "Kolkata",
    "Ahmedabad",
]

PAYMENT_TYPES = ["UPI", "Card", "NetBanking", "Wallet"]

MERCHANTS = {
    "Food": ["Swiggy", "Zomato", "Starbucks", "McDonalds"],
    "Shopping": ["Amazon", "Flipkart", "Myntra", "BigBasket"],
    "Travel": ["Uber", "Ola", "MakeMyTrip", "IRCTC"],
    "Finance": ["Groww", "Zerodha", "Paytm", "PhonePe"],
    "Entertainment": ["Netflix", "BookMyShow", "Spotify", "Hotstar"],
}


def generate_user_profiles(num_users: int = 5000) -> pd.DataFrame:
    users = []

    all_merchants = [
        merchant
        for merchants in MERCHANTS.values()
        for merchant in merchants
    ]

    for i in range(1, num_users + 1):
        average_amount = round(random.uniform(300, 5000), 2)
        std_dev = round(average_amount * random.uniform(0.2, 0.7), 2)

        favorite_merchants = random.sample(all_merchants, k=5)

        start_hour = random.randint(6, 11)
        end_hour = random.randint(19, 23)

        known_devices = [
            f"D{i:05d}-A",
            f"D{i:05d}-B",
        ]

        users.append(
            {
                "user_id": f"U{i:05d}",
                "home_location": random.choice(LOCATIONS),
                "preferred_payment_type": random.choice(PAYMENT_TYPES),
                "average_transaction_amount": average_amount,
                "transaction_amount_std_dev": std_dev,
                "favorite_merchants": "|".join(favorite_merchants),
                "active_start_hour": start_hour,
                "active_end_hour": end_hour,
                "known_devices": "|".join(known_devices),
                "travel_frequency": round(random.uniform(0.02, 0.25), 2),
                "risk_tolerance": random.choice(["Low", "Medium", "High"]),
            }
        )

    return pd.DataFrame(users)


def main():
    profiles = generate_user_profiles()
    output_path = "../data/processed/user_profiles.csv"

    profiles.to_csv(output_path, index=False)

    print(f"Generated {len(profiles)} user profiles")
    print(f"Saved to {output_path}")
    print(profiles.head())


if __name__ == "__main__":
    main()