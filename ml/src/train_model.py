import pandas as pd
import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    average_precision_score,
)
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline


DATA_PATH = "../data/creditcard.csv"
MODEL_PATH = "models/fraud_model.joblib"


def main():
    df = pd.read_csv(DATA_PATH)

    # Time-based split because transaction order matters.
    # We avoid random split to reduce future-data leakage.
    split_index = int(len(df) * 0.8)

    train_df = df.iloc[:split_index]
    test_df = df.iloc[split_index:]

    X_train = train_df.drop("Class", axis=1)
    y_train = train_df["Class"]

    X_test = test_df.drop("Class", axis=1)
    y_test = test_df["Class"]

    model = Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            (
                "classifier",
                RandomForestClassifier(
                    n_estimators=100,
                    class_weight="balanced",
                    random_state=42,
                    n_jobs=-1,
                ),
            ),
        ]
    )

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, digits=4))

    print("\nPR-AUC / Average Precision Score:")
    print(average_precision_score(y_test, y_proba))

    joblib.dump(model, MODEL_PATH)
    print(f"\nModel saved to {MODEL_PATH}")


if __name__ == "__main__":
    main()