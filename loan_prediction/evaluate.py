import numpy as np
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
from sklearn.tree import plot_tree
from preprocess import load_data, preprocess_data

def load_model(filename):
    """
    load a trained model from a file directly
    """
    with open(f'models/{filename}', 'rb') as f:
        model = pickle.load(f)
    return model

def evaluate_model(model, X_test, y_test, model_name):
    """
    evaluate a model on the test set
    """
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    
    print(f"\n--- {model_name} Performance ---")
    print(f"Accuracy: {accuracy:.3f}")
    print(f"Precision: {precision:.3f}")
    print(f"Recall: {recall:.3f}")
    print(f"F1 Score: {f1:.3f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False,
                xticklabels=['Not Approved', 'Approved'],
                yticklabels=['Not Approved', 'Approved'])
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.title(f'Confusion Matrix - {model_name}')
    plt.savefig(f'models/{model_name.lower().replace(" ", "_")}_confusion_matrix.png')
    
    return {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1': f1
    }

def compare_models(knn_metrics, dt_metrics):
    """
    compare the performance of KNN and Decision Tree models
    """
    models = ['KNN', 'Decision Tree']
    metrics_df = pd.DataFrame({
        'Model': models,
        'Accuracy': [knn_metrics['accuracy'], dt_metrics['accuracy']],
        'Precision': [knn_metrics['precision'], dt_metrics['precision']],
        'Recall': [knn_metrics['recall'], dt_metrics['recall']],
        'F1 Score': [knn_metrics['f1'], dt_metrics['f1']]
    })
    print("\n--- Model Comparison ---")
    print(metrics_df)

    metrics_df_melted = pd.melt(metrics_df, id_vars='Model', var_name='Metric', value_name='Score')
    plt.figure(figsize=(12, 6))
    sns.barplot(x='Metric', y='Score', hue='Model', data=metrics_df_melted)
    plt.title('Model Comparison')
    plt.ylim(0, 1)
    plt.savefig('models/model_comparison.png')
    
    if dt_metrics['f1'] > knn_metrics['f1']:
        print("\nThe Decision Tree model performs better based on F1 score.")
        return 'Decision Tree'
    elif knn_metrics['f1'] > dt_metrics['f1']:
        print("\nThe KNN model performs better based on F1 score.")
        return 'KNN'
    else:
        print("\nBoth models perform equally based on F1 score.")
        return 'Both'

def plot_decision_tree(dt_model):
    """
    plot the decision tree for visualization
    """
    plt.figure(figsize=(20, 10))
    plot_tree(dt_model, filled=True, feature_names=['income', 'credit_score', 'loan_amount', 'loan_term', 
                                                    'employed', 'self-employed', 'unemployed'],
             class_names=['Not Approved', 'Approved'], rounded=True)
    plt.title('Decision Tree')
    plt.savefig('models/decision_tree_visualization.png')

def feature_importance(dt_model):
    """
    analyze feature importance from the Decision Tree model
    """
    feature_names = ['income', 'credit_score', 'loan_amount', 'loan_term', 
                     'employed', 'self-employed', 'unemployed']
    importances = dt_model.feature_importances_

    feature_importance_df = pd.DataFrame({
        'Feature': feature_names[:len(importances)],
        'Importance': importances
    }).sort_values('Importance', ascending=False)
    print("\n--- Feature Importance ---")
    print(feature_importance_df)
    
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Importance', y='Feature', data=feature_importance_df)
    plt.title('Feature Importance')
    plt.savefig('models/feature_importance.png')
    
    return feature_importance_df

if __name__ == "__main__":
    data = load_data('data/loan_data.csv')
    X_train, X_test, y_train, y_test, _ = preprocess_data(data)
    
    knn_model = load_model('knn_model.pkl')
    dt_model = load_model('decision_tree_model.pkl')
    
    knn_metrics = evaluate_model(knn_model, X_test, y_test, 'KNN')
    dt_metrics = evaluate_model(dt_model, X_test, y_test, 'Decision Tree')

    best_model = compare_models(knn_metrics, dt_metrics)

    if best_model == 'Decision Tree' or best_model == 'Both':
        plot_decision_tree(dt_model)
        feature_importance(dt_model)
    
    print("\nEvaluation completed. Results and visualizations saved to the models directory.")
