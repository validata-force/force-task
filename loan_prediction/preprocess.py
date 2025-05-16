import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

def load_data(filepath):
    return pd.read_csv(filepath)

def preprocess_data(data):
    data = data.dropna()
    
    X = data.drop('loan_approved', axis=1)
    y = data['loan_approved']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    numeric_features = ['income', 'credit_score', 'loan_amount', 'loan_term']
    categorical_features = ['employment_status']

    numeric_transformer = Pipeline(steps=[
        ('scaler', StandardScaler())
    ])
    categorical_transformer = Pipeline(steps=[
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ])

    X_train_processed = preprocessor.fit_transform(X_train)
    X_test_processed = preprocessor.transform(X_test)

    return X_train_processed, X_test_processed, y_train, y_test, preprocessor

if __name__ == "__main__":
    data = load_data('data/loan_data.csv')
    print("Data loaded. Shape:", data.shape)
    print("\nBasic statistics:")
    print(data.describe())
    print("\nClass distribution:")
    print(data['loan_approved'].value_counts(normalize=True))
    X_train, X_test, y_train, y_test, preprocessor = preprocess_data(data)
    print("\nData preprocessing complete.")
    print(f"Training set shape: {X_train.shape}")
    print(f"Testing set shape: {X_test.shape}")
