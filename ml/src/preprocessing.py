def split_features_target(train_df, test_df, target_column: str = "Class"):
    X_train = train_df.drop(target_column, axis=1)
    y_train = train_df[target_column]

    X_test = test_df.drop(target_column, axis=1)
    y_test = test_df[target_column]

    return X_train, y_train, X_test, y_test