from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    average_precision_score,
)


def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, digits=4))

    print("\nPR-AUC / Average Precision Score:")
    print(average_precision_score(y_test, y_proba))