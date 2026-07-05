import pandas as pd


def get_feature_importance_map(model, feature_names):
    classifier = model.named_steps["classifier"]
    importances = classifier.feature_importances_

    return dict(zip(feature_names, importances))


def generate_explanation(row, feature_importance_map, top_n=3):
    scored_features = []

    for feature, importance in feature_importance_map.items():
        value = row[feature]
        contribution_score = abs(value) * importance

        scored_features.append((feature, value, contribution_score))

    top_features = sorted(
        scored_features,
        key=lambda item: item[2],
        reverse=True
    )[:top_n]

    explanations = []

    for feature, value, _ in top_features:
        explanations.append(f"{feature} had a strong influence with value {value:.4f}")

    return "; ".join(explanations)