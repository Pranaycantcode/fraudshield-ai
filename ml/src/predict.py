import joblib
import pandas as pd


MODEL_PATH = "models/fraud_model.joblib"


def get_risk_label(score: float) -> str:
    if score >= 0.8:
        return "High Risk"
    elif score >= 0.4:
        return "Suspicious"
    return "Safe"


def predict_transactions(input_csv_path: str) -> pd.DataFrame:
    model = joblib.load(MODEL_PATH)

    df = pd.read_csv(input_csv_path)

    if "Class" in df.columns:
        features = df.drop("Class", axis=1)
    else:
        features = df.copy()

    fraud_scores = model.predict_proba(features)[:, 1]

    results = df.copy()
    results["fraud_score"] = fraud_scores
    results["risk_label"] = [get_risk_label(score) for score in fraud_scores]

    return results


def main():
    input_path = "../data/creditcard.csv"
    results = predict_transactions(input_path)

    print("\nPrediction preview:")
    print(results[["fraud_score", "risk_label"]].head(20))

    print("\nRisk label counts:")
    print(results["risk_label"].value_counts())


if __name__ == "__main__":
    main()