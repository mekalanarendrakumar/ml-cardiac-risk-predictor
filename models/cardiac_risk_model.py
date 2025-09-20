import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

class CardiacRiskPredictor:
    """
    Machine Learning model for predicting cardiac risk based on patient health data
    """
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.feature_names = [
            'age', 'sex', 'chest_pain_type', 'resting_bp', 'cholesterol',
            'fasting_blood_sugar', 'resting_ecg', 'max_heart_rate',
            'exercise_angina', 'oldpeak', 'slope', 'major_vessels', 'thalassemia'
        ]
        self.is_trained = False
        self.load_model()
    
    def generate_sample_data(self, n_samples=1000):
        """
        Generate synthetic cardiac data for demonstration purposes
        In a real-world scenario, this would be replaced with actual medical data
        """
        np.random.seed(42)
        
        data = {
            'age': np.random.normal(54, 9, n_samples).astype(int),
            'sex': np.random.choice([0, 1], n_samples),  # 0: Female, 1: Male
            'chest_pain_type': np.random.choice([0, 1, 2, 3], n_samples),
            'resting_bp': np.random.normal(131, 17, n_samples),
            'cholesterol': np.random.normal(246, 51, n_samples),
            'fasting_blood_sugar': np.random.choice([0, 1], n_samples, p=[0.85, 0.15]),
            'resting_ecg': np.random.choice([0, 1, 2], n_samples),
            'max_heart_rate': np.random.normal(149, 22, n_samples),
            'exercise_angina': np.random.choice([0, 1], n_samples, p=[0.68, 0.32]),
            'oldpeak': np.random.exponential(1, n_samples),
            'slope': np.random.choice([0, 1, 2], n_samples),
            'major_vessels': np.random.choice([0, 1, 2, 3], n_samples),
            'thalassemia': np.random.choice([0, 1, 2, 3], n_samples)
        }
        
        # Create target variable (heart disease risk)
        # This is a simplified logic for demonstration
        risk_factors = (
            (data['age'] > 60).astype(int) +
            (data['sex'] == 1).astype(int) +
            (data['chest_pain_type'] == 0).astype(int) +
            (data['resting_bp'] > 140).astype(int) +
            (data['cholesterol'] > 240).astype(int) +
            (data['fasting_blood_sugar'] == 1).astype(int) +
            (data['max_heart_rate'] < 120).astype(int) +
            (data['exercise_angina'] == 1).astype(int) +
            (data['oldpeak'] > 1.5).astype(int) +
            (data['major_vessels'] > 0).astype(int)
        )
        
        # Convert risk factors to probability and then to binary outcome
        risk_probability = 1 / (1 + np.exp(-(risk_factors - 3)))
        data['target'] = np.random.binomial(1, risk_probability, n_samples)
        
        return pd.DataFrame(data)
    
    def train_model(self):
        """Train the cardiac risk prediction model"""
        # Generate sample data
        df = self.generate_sample_data()
        
        # Prepare features and target
        X = df[self.feature_names]
        y = df['target']
        
        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Scale the features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train the model
        self.model = RandomForestClassifier(
            n_estimators=100,
            random_state=42,
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=2
        )
        
        self.model.fit(X_train_scaled, y_train)
        
        # Evaluate the model
        y_pred = self.model.predict(X_test_scaled)
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"Model trained successfully!")
        print(f"Accuracy: {accuracy:.4f}")
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred))
        
        # Save the model
        self.save_model()
        self.is_trained = True
        
        return accuracy
    
    def save_model(self):
        """Save the trained model and scaler"""
        if not os.path.exists('models/saved'):
            os.makedirs('models/saved')
        
        joblib.dump(self.model, 'models/saved/cardiac_risk_model.pkl')
        joblib.dump(self.scaler, 'models/saved/scaler.pkl')
    
    def load_model(self):
        """Load the trained model and scaler"""
        model_path = 'models/saved/cardiac_risk_model.pkl'
        scaler_path = 'models/saved/scaler.pkl'
        
        if os.path.exists(model_path) and os.path.exists(scaler_path):
            self.model = joblib.load(model_path)
            self.scaler = joblib.load(scaler_path)
            self.is_trained = True
        else:
            # Train the model if it doesn't exist
            print("Model not found. Training new model...")
            self.train_model()
    
    def predict_risk(self, patient_data):
        """
        Predict cardiac risk for a single patient
        
        Args:
            patient_data (dict): Dictionary containing patient features
        
        Returns:
            float: Risk probability (0-1)
        """
        if not self.is_trained:
            raise ValueError("Model is not trained yet!")
        
        # Convert to DataFrame
        df = pd.DataFrame([patient_data])
        
        # Ensure all features are present
        for feature in self.feature_names:
            if feature not in df.columns:
                raise ValueError(f"Missing feature: {feature}")
        
        # Scale the features
        X_scaled = self.scaler.transform(df[self.feature_names])
        
        # Predict probability
        risk_probability = self.model.predict_proba(X_scaled)[0][1]
        
        return round(risk_probability, 4)
    
    def get_risk_level(self, probability):
        """
        Convert probability to risk level
        
        Args:
            probability (float): Risk probability
        
        Returns:
            str: Risk level description
        """
        if probability < 0.3:
            return "Low Risk"
        elif probability < 0.6:
            return "Moderate Risk"
        elif probability < 0.8:
            return "High Risk"
        else:
            return "Very High Risk"
    
    def get_feature_importance(self):
        """Get feature importance from the trained model"""
        if not self.is_trained:
            return None
        
        importance = self.model.feature_importances_
        feature_importance = dict(zip(self.feature_names, importance))
        
        # Sort by importance
        return dict(sorted(feature_importance.items(), key=lambda x: x[1], reverse=True))

if __name__ == "__main__":
    # Test the model
    predictor = CardiacRiskPredictor()
    
    # Example patient data
    test_patient = {
        'age': 45,
        'sex': 1,
        'chest_pain_type': 2,
        'resting_bp': 130,
        'cholesterol': 250,
        'fasting_blood_sugar': 0,
        'resting_ecg': 0,
        'max_heart_rate': 150,
        'exercise_angina': 0,
        'oldpeak': 1.2,
        'slope': 1,
        'major_vessels': 0,
        'thalassemia': 2
    }
    
    risk = predictor.predict_risk(test_patient)
    risk_level = predictor.get_risk_level(risk)
    
    print(f"\nTest Prediction:")
    print(f"Risk Probability: {risk}")
    print(f"Risk Level: {risk_level}")
    
    print(f"\nFeature Importance:")
    importance = predictor.get_feature_importance()
    for feature, imp in importance.items():
        print(f"{feature}: {imp:.4f}")