import numpy as np
import pandas as pd
import pickle
import os
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import GridSearchCV
from preprocess import load_data, preprocess_data

def train_knn(X_train, y_train):
    """
    train a K-Nearest Neighbors model with hyperparameter tuning
    """
    print("Training KNN model with hyperparameter tuning...")

    param_grid = {
        'n_neighbors': [3, 5, 7, 9, 11],
        'weights': ['uniform', 'distance'],
        'metric': ['euclidean', 'manhattan', 'minkowski']
    }
    knn = KNeighborsClassifier()
    grid_search = GridSearchCV(knn, param_grid, cv=5, scoring='f1', n_jobs=-1)
    grid_search.fit(X_train, y_train)

    print(f"Best parameters: {grid_search.best_params_}")
    print(f"Best cross-validation score: {grid_search.best_score_:.3f}")

    best_knn = grid_search.best_estimator_

    return best_knn

def train_decision_tree(X_train, y_train):
    """
    train a Decision Tree model with hyperparameter tuning
    """
    print("Training Decision Tree model with hyperparameter tuning...")

    param_grid = {
        'max_depth': [None, 5, 10, 15, 20],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4],
        'criterion': ['gini', 'entropy']
    }

    dt = DecisionTreeClassifier(random_state=42)

    grid_search = GridSearchCV(dt, param_grid, cv=5, scoring='f1', n_jobs=-1)
    grid_search.fit(X_train, y_train)

    print(f"Best parameters: {grid_search.best_params_}")
    print(f"Best cross-validation score: {grid_search.best_score_:.3f}")

    best_dt = grid_search.best_estimator_

    return best_dt

def save_model(model, filename):
    """
    save the trained model to a file
    """
    os.makedirs('models', exist_ok=True)

    with open(f'models/{filename}', 'wb') as f:
        pickle.dump(model, f)

    print(f"Model saved as models/{filename}")

if __name__ == "__main__":
    data = load_data('data/loan_data.csv')
    X_train, X_test, y_train, y_test, preprocessor = preprocess_data(data)
    save_model(preprocessor, 'preprocessor.pkl')
    knn_model = train_knn(X_train, y_train)
    save_model(knn_model, 'knn_model.pkl')
    dt_model = train_decision_tree(X_train, y_train)
    save_model(dt_model, 'decision_tree_model.pkl')
