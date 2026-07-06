import pandas as pd
import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, average_precision_score
from sklearn.model_selection import train_test_split

from feature_engineering import engineer_transaction_features
from labeling import assign_synthetic_label


INPUT_PATH = "../data/sample/transactions_sample.csv"
MODEL_PATH = "models/realistic_fraud_model.joblib"

FEATURE_COLUMNS = [
    "amount_to_user_avg_ratio",
    "is_unusual_hour",
    "is_new_location",
    "is_new_device",
    "is_unknown_merchant",
    "user_transaction_count",
]


def main():
    df = pd.read_csv(INPUT_PATH)

    engineered_df = engineer_transaction_features(df)
    engineered_df["label"] = engineered_df.apply(assign_synthetic_label, axis=1)

    X = engineered_df[FEATURE_COLUMNS]
    y = engineered_df["label"]

    if y.nunique() < 2:
        raise ValueError("Training data must contain both safe and fraud-like examples.")

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.3,
        random_state=42,
        stratify=y,
    )

    model = RandomForestClassifier(
        n_estimators=100,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1,
    )

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, digits=4))

    print("\nPR-AUC:")
    print(average_precision_score(y_test, y_proba))

    joblib.dump(model, MODEL_PATH)
    print(f"\nModel saved to {MODEL_PATH}")


if __name__ == "__main__":
    main()