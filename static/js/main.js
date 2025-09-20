// Main JavaScript for Cardiac Risk Predictor

document.addEventListener('DOMContentLoaded', function() {
    // Form validation and enhancement
    const form = document.getElementById('predictionForm');
    if (form) {
        initializeForm(form);
    }
    
    // Add smooth scrolling for anchor links
    addSmoothScrolling();
    
    // Add form field validation
    addFieldValidation();
    
    // Add loading states
    addLoadingStates();
});

function initializeForm(form) {
    // Add real-time validation
    const inputs = form.querySelectorAll('input, select');
    inputs.forEach(input => {
        input.addEventListener('blur', validateField);
        input.addEventListener('input', clearFieldError);
    });
    
    // Handle form submission
    form.addEventListener('submit', function(e) {
        if (!validateForm()) {
            e.preventDefault();
            showFormErrors();
        } else {
            showLoadingState();
        }
    });
    
    // Add helpful tooltips or info
    addFieldTooltips();
}

function validateField(event) {
    const field = event.target;
    const value = field.value.trim();
    let isValid = true;
    let errorMessage = '';
    
    // Required field validation
    if (field.hasAttribute('required') && !value) {
        isValid = false;
        errorMessage = 'This field is required';
    }
    
    // Specific field validations
    switch (field.name) {
        case 'age':
            if (value && (value < 1 || value > 120)) {
                isValid = false;
                errorMessage = 'Age must be between 1 and 120 years';
            }
            break;
            
        case 'resting_bp':
            if (value && (value < 50 || value > 250)) {
                isValid = false;
                errorMessage = 'Blood pressure must be between 50 and 250 mmHg';
            }
            break;
            
        case 'cholesterol':
            if (value && (value < 100 || value > 600)) {
                isValid = false;
                errorMessage = 'Cholesterol must be between 100 and 600 mg/dl';
            }
            break;
            
        case 'max_heart_rate':
            if (value && (value < 60 || value > 220)) {
                isValid = false;
                errorMessage = 'Heart rate must be between 60 and 220 bpm';
            }
            break;
            
        case 'oldpeak':
            if (value && (value < 0 || value > 10)) {
                isValid = false;
                errorMessage = 'Oldpeak must be between 0 and 10';
            }
            break;
    }
    
    // Display validation result
    if (!isValid) {
        showFieldError(field, errorMessage);
    } else {
        clearFieldError(field);
    }
    
    return isValid;
}

function showFieldError(field, message) {
    // Remove existing error
    clearFieldError(field);
    
    // Add error class
    field.classList.add('error');
    
    // Create error message
    const errorElement = document.createElement('span');
    errorElement.className = 'error-message';
    errorElement.textContent = message;
    
    // Insert error message after the field
    field.parentNode.appendChild(errorElement);
}

function clearFieldError(field) {
    if (typeof field === 'object' && field.target) {
        field = field.target;
    }
    
    field.classList.remove('error');
    const errorElement = field.parentNode.querySelector('.error-message');
    if (errorElement) {
        errorElement.remove();
    }
}

function validateForm() {
    const form = document.getElementById('predictionForm');
    const inputs = form.querySelectorAll('input[required], select[required]');
    let isValid = true;
    
    inputs.forEach(input => {
        if (!validateField({ target: input })) {
            isValid = false;
        }
    });
    
    return isValid;
}

function showFormErrors() {
    // Scroll to first error
    const firstError = document.querySelector('.error');
    if (firstError) {
        firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
        firstError.focus();
    }
    
    // Show general error message
    showNotification('Please correct the errors in the form before submitting.', 'error');
}

function showLoadingState() {
    const submitButton = document.querySelector('.btn-predict');
    if (submitButton) {
        submitButton.textContent = 'Analyzing...';
        submitButton.disabled = true;
        
        // Add loading spinner
        const spinner = document.createElement('span');
        spinner.className = 'loading-spinner';
        spinner.innerHTML = ' ⟳';
        submitButton.appendChild(spinner);
    }
}

function addFieldTooltips() {
    const tooltips = {
        'chest_pain_type': 'Type of chest pain: Typical angina is classic heart-related pain, while asymptomatic means no chest pain',
        'fasting_blood_sugar': 'Blood sugar level after fasting - above 120 mg/dl may indicate diabetes risk',
        'resting_ecg': 'Electrocardiogram results when at rest - shows heart rhythm and electrical activity',
        'exercise_angina': 'Chest pain that occurs during physical exercise or exertion',
        'oldpeak': 'ST depression induced by exercise relative to rest - measure of heart stress during exercise',
        'slope': 'The slope of the peak exercise ST segment - indicates heart response to exercise',
        'major_vessels': 'Number of major blood vessels colored by fluoroscopy (0-3)',
        'thalassemia': 'Blood disorder affecting hemoglobin - can impact heart health'
    };
    
    Object.keys(tooltips).forEach(fieldName => {
        const field = document.querySelector(`[name="${fieldName}"]`);
        if (field) {
            const label = field.parentNode.querySelector('label');
            if (label) {
                label.title = tooltips[fieldName];
                label.style.cursor = 'help';
                
                // Add info icon
                const infoIcon = document.createElement('span');
                infoIcon.innerHTML = ' ℹ️';
                infoIcon.style.fontSize = '0.8em';
                infoIcon.title = tooltips[fieldName];
                label.appendChild(infoIcon);
            }
        }
    });
}

function addSmoothScrolling() {
    const links = document.querySelectorAll('a[href^="#"]');
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

function addFieldValidation() {
    // Add CSS for validation styles if not already present
    if (!document.querySelector('#validation-styles')) {
        const style = document.createElement('style');
        style.id = 'validation-styles';
        style.textContent = `
            .error {
                border-color: #e74c3c !important;
                background-color: #fdf2f2;
            }
            
            .error-message {
                color: #e74c3c;
                font-size: 0.9em;
                margin-top: 0.25rem;
                display: block;
            }
            
            .loading-spinner {
                animation: spin 1s linear infinite;
                display: inline-block;
            }
            
            @keyframes spin {
                from { transform: rotate(0deg); }
                to { transform: rotate(360deg); }
            }
            
            .notification {
                position: fixed;
                top: 20px;
                right: 20px;
                padding: 1rem;
                border-radius: 5px;
                z-index: 1000;
                max-width: 300px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }
            
            .notification.error {
                background: #fdf2f2;
                border: 1px solid #f5c6cb;
                color: #721c24;
            }
            
            .notification.success {
                background: #d4edda;
                border: 1px solid #c3e6cb;
                color: #155724;
            }
        `;
        document.head.appendChild(style);
    }
}

function addLoadingStates() {
    // Add loading state for any AJAX calls if implemented later
    const buttons = document.querySelectorAll('button[type="submit"]');
    buttons.forEach(button => {
        button.addEventListener('click', function() {
            // Prevent double submission
            if (this.disabled) return false;
            
            setTimeout(() => {
                this.disabled = true;
            }, 100);
        });
    });
}

function showNotification(message, type = 'info') {
    // Remove existing notifications
    const existing = document.querySelectorAll('.notification');
    existing.forEach(el => el.remove());
    
    // Create notification
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    
    // Add to page
    document.body.appendChild(notification);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        notification.remove();
    }, 5000);
    
    // Add click to dismiss
    notification.addEventListener('click', () => {
        notification.remove();
    });
}

// Utility functions for potential API integration
function makeAPIRequest(endpoint, data) {
    return fetch(endpoint, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .catch(error => {
        console.error('API Error:', error);
        showNotification('An error occurred while processing your request.', 'error');
    });
}

// Export functions for potential testing or external use
window.CardiacRiskPredictor = {
    validateField,
    validateForm,
    showNotification,
    makeAPIRequest
};