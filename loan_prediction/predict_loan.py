import pickle
import os
import numpy as np
import pandas as pd

def load_models():
    models_dir = os.path.join(os.path.dirname(__file__), 'models')
    
    with open(os.path.join(models_dir, 'preprocessor.pkl'), 'rb') as f:
        preprocessor = pickle.load(f)
    
    with open(os.path.join(models_dir, 'knn_model.pkl'), 'rb') as f:
        knn_model = pickle.load(f)
    
    with open(os.path.join(models_dir, 'decision_tree_model.pkl'), 'rb') as f:
        dt_model = pickle.load(f)
    
    return preprocessor, knn_model, dt_model

def get_user_input():
    print("\n===== Loan Approval Prediction System =====")
    print("Please enter the following information about the loan application:")
    
    try:
        income = float(input("\nAnnual Income (e.g., 50000): $"))
        credit_score = int(input("Credit Score (e.g., 650): "))
        loan_amount = float(input("Loan Amount (e.g., 15000): $"))
        loan_term = int(input("Loan Term in months (e.g., 36): "))
        
        print("\nEmployment Status:")
        print("1. Employed")
        print("2. Self-employed")
        print("3. Unemployed")
        
        status_choice = int(input("Select employment status (1-3): "))
        
        if status_choice == 1:
            employment_status = "employed"
        elif status_choice == 2:
            employment_status = "self-employed"
        elif status_choice == 3:
            employment_status = "unemployed"
        else:
            print("Invalid choice. Defaulting to employed.")
            employment_status = "employed"
        
        return {
            'income': income,
            'credit_score': credit_score,
            'loan_amount': loan_amount,
            'loan_term': loan_term,
            'employment_status': employment_status
        }
    except ValueError:
        print("Error: Please enter valid numbers for the financial information.")
        return None

def predict_loan_approval(loan_data, preprocessor, knn_model, dt_model):
    df = pd.DataFrame([loan_data])
    
    X = preprocessor.transform(df)
    
    knn_pred = knn_model.predict(X)[0]
    knn_prob = knn_model.predict_proba(X)[0][1]
    
    dt_pred = dt_model.predict(X)[0]
    dt_prob = dt_model.predict_proba(X)[0][1]
    
    return {
        'knn_prediction': knn_pred,
        'knn_probability': knn_prob,
        'dt_prediction': dt_pred,
        'dt_probability': dt_prob
    }

def display_results(loan_data, predictions):
    print("\n===== Loan Application Analysis =====")
    print(f"Income: ${loan_data['income']:,.2f}")
    print(f"Credit Score: {loan_data['credit_score']}")
    print(f"Loan Amount: ${loan_data['loan_amount']:,.2f}")
    print(f"Loan Term: {loan_data['loan_term']} months")
    print(f"Employment Status: {loan_data['employment_status'].capitalize()}")
    
    print("\n===== Prediction Results =====")
    
    print("\nBased on our Decision Tree model (our most accurate model):")
    if predictions['dt_prediction'] == 1:
        print(f"APPROVED with {predictions['dt_probability']*100:.1f}% confidence")
    else:
        print(f"NOT APPROVED with {(1-predictions['dt_probability'])*100:.1f}% confidence")
    
    print("\nSecond opinion from our KNN model:")
    if predictions['knn_prediction'] == 1:
        print(f"APPROVED with {predictions['knn_probability']*100:.1f}% confidence")
    else:
        print(f"NOT APPROVED with {(1-predictions['knn_probability'])*100:.1f}% confidence")
    
    explain_result(loan_data, predictions)

def explain_result(loan_data, predictions):
    print("\n===== Analysis =====")
    
    if loan_data['income'] >= 60000:
        print("POSITIVE: Your income is favorable for loan approval")
    elif loan_data['income'] >= 40000:
        print("NEUTRAL: Your income is acceptable for loan consideration")
    else:
        print("CONCERN: Your income may be below the preferred threshold")
    
    if loan_data['credit_score'] >= 700:
        print("POSITIVE: Your credit score is excellent")
    elif loan_data['credit_score'] >= 650:
        print("NEUTRAL: Your credit score is reasonable")
    else:
        print("CONCERN: Your credit score may need improvement")
    
    loan_to_income = loan_data['loan_amount'] / loan_data['income']
    if loan_to_income <= 0.3:
        print("POSITIVE: Your loan amount to income ratio is healthy")
    elif loan_to_income <= 0.5:
        print("NEUTRAL: Your loan amount is reasonable compared to your income")
    else:
        print("CONCERN: Your requested loan amount is high relative to your income")
    
    if loan_data['employment_status'] == 'employed':
        print("POSITIVE: Being employed is favorable for loan approval")
    elif loan_data['employment_status'] == 'self-employed':
        print("NEUTRAL: Being self-employed is considered in loan decisions")
    else:
        print("CONCERN: Being unemployed may make loan approval challenging")
    
    print("\nRemember: This is just a prediction model and not a final decision from a bank.")
    print("Actual loan approvals may consider additional factors not included in this model.")

def main():
    try:
        preprocessor, knn_model, dt_model = load_models()
        
        while True:
            loan_data = get_user_input()
            if not loan_data:
                continue
            
            predictions = predict_loan_approval(loan_data, preprocessor, knn_model, dt_model)
            
            display_results(loan_data, predictions)
            
            another = input("\nWould you like to predict another loan? (yes/no): ").lower()
            if another != 'yes' and another != 'y':
                print("\nThank you for using the Loan Approval Prediction System!")
                break
    
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please make sure you've trained the models first by running:")
        print("1. python preprocess.py")
        print("2. python train.py")
        print("3. python evaluate.py")

if __name__ == "__main__":
    main() 