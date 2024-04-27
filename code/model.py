import optuna
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.metrics import mean_squared_error


# We assume that the data is missing at random
def impute(df, method='mean'):
    columns = df.columns
    for column in columns:
        if df[column].isnull().sum() > 0:
            print(column)
            if method == 'mean':
                df[column] = df[column].fillna(df[column].mean())
            elif method == 'median':
                df[column] = df[column].fillna(df[column].median())
            elif method == 'mode':
                df[column] = df[column].fillna(df[column].mode()[0])

    return df


def time_based_split(df, date_column, split_ratio=0.8):
    df[date_column] = pd.to_datetime(df[date_column])
    df = df.sort_values(by=date_column)
    split_index = int(len(df) * split_ratio)
    train = df[:split_index]
    test = df[split_index:]
    return train, test

def model(data, feature):

    df = data
    features = feature
    
    # Optuna objective function
    def objective(trial):
        nonlocal df, features
        df[features] = impute(df[features], method='mean')
        
        # Split the data
        train, test = time_based_split(df, 'period_end_date', split_ratio=0.8)
        train_features = train[features]
        test_features = test[features]

        
        # Suggest parameters for Isolation Forest
        n_estimators = trial.suggest_int('n_estimators', 50, 300)
        max_samples = trial.suggest_int('max_samples', 10, len(train_features))
        contamination = trial.suggest_uniform('contamination', 0.01, 0.1)
        max_features = trial.suggest_uniform('max_features', 0.1, 1.0)
        
        # Create and train Isolation Forest
        clf = IsolationForest(n_estimators=n_estimators, max_samples=max_samples,
                            contamination=contamination, max_features=max_features, random_state=42)
        clf.fit(train_features)
        
        # Predict on test data
        y_pred = clf.predict(test_features)
        y_pred = np.where(y_pred == 1, 0, 1)  # Convert from (-1, 1) to (0, 1) where 1 represents anomalies

        # Since there are no true labels, use a placeholder metric or implement unsupervised metrics
        # For demonstration, let's assume a synthetic scenario:
        y_test = np.random.randint(0, 2, size=len(test_features))  # Synthetic labels for demonstration
        score = mean_squared_error(y_test, y_pred)
        
        return score

    # Create a study object and optimize the objective function
    study = optuna.create_study(direction='minimize')
    study.optimize(objective, n_trials=50)