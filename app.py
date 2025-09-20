from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
from models.cardiac_risk_model import CardiacRiskPredictor
import joblib
import os

app = Flask(__name__)

# Initialize the cardiac risk predictor
predictor = CardiacRiskPredictor()

@app.route('/')
def index():
    """Main page with prediction form"""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Handle prediction requests"""
    try:
        # Get form data
        data = {
            'age': float(request.form['age']),
            'sex': int(request.form['sex']),
            'chest_pain_type': int(request.form['chest_pain_type']),
            'resting_bp': float(request.form['resting_bp']),
            'cholesterol': float(request.form['cholesterol']),
            'fasting_blood_sugar': int(request.form['fasting_blood_sugar']),
            'resting_ecg': int(request.form['resting_ecg']),
            'max_heart_rate': float(request.form['max_heart_rate']),
            'exercise_angina': int(request.form['exercise_angina']),
            'oldpeak': float(request.form['oldpeak']),
            'slope': int(request.form['slope']),
            'major_vessels': int(request.form['major_vessels']),
            'thalassemia': int(request.form['thalassemia'])
        }
        
        # Make prediction
        risk_probability = predictor.predict_risk(data)
        risk_level = predictor.get_risk_level(risk_probability)
        
        return render_template('result.html', 
                             risk_probability=risk_probability,
                             risk_level=risk_level,
                             patient_data=data)
    
    except Exception as e:
        return render_template('error.html', error=str(e))

@app.route('/api/predict', methods=['POST'])
def api_predict():
    """API endpoint for predictions"""
    try:
        data = request.get_json()
        risk_probability = predictor.predict_risk(data)
        risk_level = predictor.get_risk_level(risk_probability)
        
        return jsonify({
            'risk_probability': risk_probability,
            'risk_level': risk_level,
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 400

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)