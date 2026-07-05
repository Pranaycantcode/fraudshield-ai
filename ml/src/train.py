import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from data_loader import load_creditcard_data, time_based_split
from preprocessing import split_features_target
from evaluate import evaluate_model


DATA_PATH = "../data/creditcard.csv"
MODEL_PATH = "models/fraud_model.joblib"


def build_model():
    return Pipeline(
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


def main():
    df = load_creditcard_data(DATA_PATH)

    train_df, test_df = time_based_split(df)

    X_train, y_train, X_test, y_test = split_features_target(train_df, test_df)

    model = build_model()
    model.fit(X_train, y_train)

    evaluate_model(model, X_test, y_test)

    joblib.dump(model, MODEL_PATH)
    print(f"\nModel saved to {MODEL_PATH}")


if __name__ == "__main__":
    main()