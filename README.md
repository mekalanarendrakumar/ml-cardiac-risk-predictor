# Cardiac Risk Predictor

This project is an ML-based cardiac risk score predictor that analyzes patient health data and applies machine learning algorithms to estimate the risk of heart-related diseases, aiming to support early diagnosis and preventive healthcare.

## Features

- **Machine Learning Model**: Uses Random Forest algorithm for cardiac risk prediction
- **Web Interface**: User-friendly Flask web application
- **Real-time Predictions**: Instant risk assessment based on patient data
- **Risk Categorization**: Classifies risk into Low, Moderate, High, and Very High categories
- **Responsive Design**: Works on desktop and mobile devices
- **Educational Purpose**: Designed for learning and demonstration

## Technology Stack

### Backend
- Python 3.x
- Flask Web Framework
- Scikit-learn for machine learning
- Pandas and NumPy for data processing
- Joblib for model persistence

### Frontend
- HTML5 & CSS3
- JavaScript for form validation
- Responsive design with CSS Grid and Flexbox
- Jinja2 templating

### Machine Learning
- Random Forest Classifier
- Feature scaling with StandardScaler
- Synthetic data generation for demonstration
- Model evaluation and validation

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/mekalanarendrakumar/ml-cardiac-risk-predictor.git
   cd ml-cardiac-risk-predictor
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open your browser** and navigate to `http://localhost:5000`

## Usage

### Web Interface

1. Navigate to the main page
2. Fill in the patient information form with the following parameters:
   - Age (1-120 years)
   - Sex (Male/Female)
   - Chest Pain Type (Typical Angina, Atypical Angina, Non-Anginal Pain, Asymptomatic)
   - Resting Blood Pressure (50-250 mmHg)
   - Cholesterol Level (100-600 mg/dl)
   - Fasting Blood Sugar (>120 mg/dl: Yes/No)
   - Resting ECG Results (Normal, ST-T Wave Abnormality, Left Ventricular Hypertrophy)
   - Maximum Heart Rate (60-220 bpm)
   - Exercise Induced Angina (Yes/No)
   - ST Depression (Oldpeak) (0-10)
   - Slope of Peak Exercise ST Segment (Upsloping, Flat, Downsloping)
   - Number of Major Vessels (0-3)
   - Thalassemia (Normal, Fixed Defect, Reversible Defect, Irreversible Defect)

3. Click "Predict Risk" to get the assessment
4. View the results including risk probability and risk level

### API Usage

The application also provides a REST API endpoint:

```bash
POST /api/predict
Content-Type: application/json

{
    "age": 45,
    "sex": 1,
    "chest_pain_type": 2,
    "resting_bp": 130,
    "cholesterol": 250,
    "fasting_blood_sugar": 0,
    "resting_ecg": 0,
    "max_heart_rate": 150,
    "exercise_angina": 0,
    "oldpeak": 1.2,
    "slope": 1,
    "major_vessels": 0,
    "thalassemia": 2
}
```

Response:
```json
{
    "risk_probability": 0.3456,
    "risk_level": "Moderate Risk",
    "status": "success"
}
```

## Model Information

### Features Used
The model uses 13 clinical features to predict cardiac risk:

1. **Age**: Patient's age in years
2. **Sex**: Biological sex (0: Female, 1: Male)
3. **Chest Pain Type**: Type of chest pain (0-3)
4. **Resting Blood Pressure**: Resting blood pressure in mmHg
5. **Cholesterol**: Serum cholesterol in mg/dl
6. **Fasting Blood Sugar**: Fasting blood sugar > 120 mg/dl (0: No, 1: Yes)
7. **Resting ECG**: Resting electrocardiographic results (0-2)
8. **Maximum Heart Rate**: Maximum heart rate achieved
9. **Exercise Angina**: Exercise induced angina (0: No, 1: Yes)
10. **Oldpeak**: ST depression induced by exercise relative to rest
11. **Slope**: Slope of the peak exercise ST segment (0-2)
12. **Major Vessels**: Number of major vessels colored by fluoroscopy (0-3)
13. **Thalassemia**: Blood disorder type (0-3)

### Model Performance
- Algorithm: Random Forest Classifier
- Features: 13 clinical parameters
- Training: Synthetic data with realistic patterns
- Evaluation: Cross-validation and test set evaluation

### Risk Categories
- **Low Risk**: < 30% probability
- **Moderate Risk**: 30-60% probability
- **High Risk**: 60-80% probability
- **Very High Risk**: > 80% probability

## Project Structure

```
ml-cardiac-risk-predictor/
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── README.md                      # Project documentation
├── models/
│   ├── cardiac_risk_model.py      # ML model implementation
│   └── saved/                     # Saved model files (created at runtime)
├── templates/
│   ├── index.html                 # Main prediction form
│   ├── result.html               # Results display
│   ├── about.html                # About page
│   └── error.html                # Error page
├── static/
│   ├── css/
│   │   └── style.css             # Stylesheet
│   └── js/
│       └── main.js               # JavaScript functionality
└── data/                         # Data directory (for future use)
```

## Important Disclaimers

⚠️ **Medical Disclaimer**: This tool is for educational and demonstration purposes only. It is not intended to replace professional medical advice, diagnosis, or treatment. Always consult with qualified healthcare professionals for proper medical evaluation and treatment.

⚠️ **Data Privacy**: Do not input real patient data. This is a demonstration application and should not be used with actual medical information.

⚠️ **Research Purpose**: The model uses synthetic data for demonstration. In a real-world application, it would need to be trained and validated on actual clinical datasets with proper medical oversight.
