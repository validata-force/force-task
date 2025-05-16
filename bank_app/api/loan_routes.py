from flask import Blueprint, request, jsonify, render_template, flash, redirect, url_for
import pickle
import numpy as np
import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'loan_prediction'))

loan_bp = Blueprint('loan', __name__, url_prefix='/loan')

model_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'loan_prediction/models')

def load_models():
    """Load the preprocessor and models for prediction"""
    try:
        with open(os.path.join(model_dir, 'preprocessor.pkl'), 'rb') as f:
            preprocessor = pickle.load(f)
        
        with open(os.path.join(model_dir, 'knn_model.pkl'), 'rb') as f:
            knn_model = pickle.load(f)
            
        with open(os.path.join(model_dir, 'decision_tree_model.pkl'), 'rb') as f:
            dt_model = pickle.load(f)
            
        return preprocessor, knn_model, dt_model
    except FileNotFoundError:
        return None, None, None

@loan_bp.route('/')
def index():
    """Loan prediction form page"""
    return render_template('loan_form.html')

@loan_bp.route('/predict', methods=['POST'])
def predict():
    """Process loan prediction from form"""
    if request.method == 'POST':
        try:
            income = float(request.form.get('income'))
            credit_score = float(request.form.get('credit_score'))
            loan_amount = float(request.form.get('loan_amount'))
            loan_term = float(request.form.get('loan_term'))
            employment_status = request.form.get('employment_status')
            
            preprocessor, knn_model, dt_model = load_models()
            
            if None in (preprocessor, knn_model, dt_model):
                flash('Models not found. Please train the models first.', 'error')
                return redirect(url_for('loan.index'))
            
            data = {
                'income': [income],
                'credit_score': [credit_score],
                'loan_amount': [loan_amount],
                'loan_term': [loan_term],
                'employment_status': [employment_status]
            }
            
            import pandas as pd
            input_df = pd.DataFrame(data)
            
            X_processed = preprocessor.transform(input_df)
            
            knn_pred = knn_model.predict(X_processed)[0]
            dt_pred = dt_model.predict(X_processed)[0]
            
            knn_prob = knn_model.predict_proba(X_processed)[0][1]
            dt_prob = dt_model.predict_proba(X_processed)[0][1]
            
            avg_prob = (knn_prob + dt_prob) / 2
            
            if knn_pred == dt_pred:
                final_pred = "Approved" if knn_pred == 1 else "Rejected"
                agreement = "Both models agree"
            else:
                final_pred = "Approved" if avg_prob > 0.5 else "Rejected"
                agreement = "Models disagree, using average probability"
            
            result = {
                'prediction': final_pred,
                'knn_prediction': "Approved" if knn_pred == 1 else "Rejected",
                'dt_prediction': "Approved" if dt_pred == 1 else "Rejected",
                'probability': f"{avg_prob:.2f}",
                'agreement': agreement
            }
            
            return render_template('loan_result.html', result=result, loan_data=data)
            
        except ValueError:
            flash('Please enter valid numeric values for income, credit score, loan amount, and loan term.', 'error')
            return redirect(url_for('loan.index'))
        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'error')
            return redirect(url_for('loan.index'))

@loan_bp.route('/api/predict', methods=['POST'])
def predict_api():
    """API endpoint for loan prediction"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        required_fields = ['income', 'credit_score', 'loan_amount', 'loan_term', 'employment_status']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        preprocessor, knn_model, dt_model = load_models()
        
        if None in (preprocessor, knn_model, dt_model):
            return jsonify({'error': 'Models not found. Please train the models first.'}), 500
        
        import pandas as pd
        input_df = pd.DataFrame({
            'income': [float(data['income'])],
            'credit_score': [float(data['credit_score'])],
            'loan_amount': [float(data['loan_amount'])],
            'loan_term': [float(data['loan_term'])],
            'employment_status': [data['employment_status']]
        })
        
        X_processed = preprocessor.transform(input_df)
        
        knn_pred = knn_model.predict(X_processed)[0]
        dt_pred = dt_model.predict(X_processed)[0]
        
        knn_prob = knn_model.predict_proba(X_processed)[0][1]
        dt_prob = dt_model.predict_proba(X_processed)[0][1]
        
        avg_prob = (knn_prob + dt_prob) / 2
        
        return jsonify({
            'prediction': "Approved" if (knn_pred + dt_pred) / 2 > 0.5 else "Rejected",
            'knn_prediction': "Approved" if knn_pred == 1 else "Rejected",
            'dt_prediction': "Approved" if dt_pred == 1 else "Rejected",
            'probability': round(avg_prob, 2)
        })
        
    except ValueError:
        return jsonify({'error': 'Invalid numeric values provided'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500 