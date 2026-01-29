"""
Flask application for serving Olympic Countries Efficiency predictions.
"""

import os
import json
import logging
import pickle
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configuration
MODEL_PATH = os.getenv('MODEL_PATH', 'models/best_model.pkl')
SCALER_PATH = os.getenv('SCALER_PATH', 'models/scaler.pkl')
FEATURE_NAMES_PATH = os.getenv('FEATURE_NAMES_PATH', 'models/feature_names.pkl')

# Global variables for model and scaler
model = None
scaler = None
feature_names = None


def load_model():
    """Load the trained model, scaler, and feature names."""
    global model, scaler, feature_names
    
    try:
        if os.path.exists(MODEL_PATH):
            with open(MODEL_PATH, 'rb') as f:
                model = pickle.load(f)
            logger.info(f"Model loaded from {MODEL_PATH}")
        else:
            logger.warning(f"Model file not found at {MODEL_PATH}")
            
        if os.path.exists(SCALER_PATH):
            with open(SCALER_PATH, 'rb') as f:
                scaler = pickle.load(f)
            logger.info(f"Scaler loaded from {SCALER_PATH}")
            
        if os.path.exists(FEATURE_NAMES_PATH):
            with open(FEATURE_NAMES_PATH, 'rb') as f:
                feature_names = pickle.load(f)
            logger.info(f"Feature names loaded from {FEATURE_NAMES_PATH}")
            
    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")
        raise


@app.before_request
def before_request():
    """Load model on first request if not already loaded."""
    if model is None:
        load_model()


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    try:
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'model_loaded': model is not None
        }), 200
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500


@app.route('/info', methods=['GET'])
def info():
    """Get model and API information."""
    return jsonify({
        'app_name': 'Olympic Countries Efficiency Prediction API',
        'version': '0.1.0',
        'model_type': type(model).__name__ if model else 'Not loaded',
        'features': feature_names.tolist() if feature_names is not None else [],
        'endpoints': {
            '/health': 'GET - Health check',
            '/info': 'GET - API information',
            '/predict': 'POST - Single prediction',
            '/predict_batch': 'POST - Batch predictions'
        }
    }), 200


@app.route('/predict', methods=['POST'])
def predict():
    """
    Make a single prediction.
    
    Expected JSON input:
    {
        "population": float,
        "gdp_per_capita": float,
        "athletes_sent": int,
        "sports_participated": int,
        "events_participated": int,
        "female_athlete_percentage": float,
        ...
    }
    """
    try:
        if model is None:
            return jsonify({
                'error': 'Model not loaded',
                'status': 'error'
            }), 500
            
        # Get JSON data
        data = request.get_json()
        
        if not data:
            return jsonify({
                'error': 'No input data provided',
                'status': 'error'
            }), 400
        
        # Create DataFrame with input features
        input_df = pd.DataFrame([data])
        
        # Select only the features used during training
        if feature_names is not None:
            # Ensure all required features are present
            missing_features = set(feature_names) - set(input_df.columns)
            if missing_features:
                return jsonify({
                    'error': f'Missing required features: {list(missing_features)}',
                    'required_features': feature_names.tolist(),
                    'status': 'error'
                }), 400
            
            input_df = input_df[feature_names]
        
        # Scale features if scaler is available
        if scaler is not None:
            input_scaled = scaler.transform(input_df)
        else:
            input_scaled = input_df.values
        
        # Make prediction
        prediction = model.predict(input_scaled)
        
        # Handle different prediction types
        if isinstance(prediction, np.ndarray):
            if prediction.ndim > 1 and prediction.shape[1] > 1:
                # Multi-class classification
                prediction_value = prediction[0]
                probabilities = prediction[0].tolist()
                result = {
                    'prediction': float(probabilities[np.argmax(probabilities)]),
                    'probabilities': probabilities,
                    'class_index': int(np.argmax(probabilities)),
                    'confidence': float(np.max(probabilities))
                }
            else:
                # Regression or binary classification
                result = {
                    'prediction': float(prediction[0])
                }
        else:
            result = {
                'prediction': float(prediction)
            }
        
        return jsonify({
            'status': 'success',
            'input': data,
            'output': result,
            'timestamp': datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500


@app.route('/predict_batch', methods=['POST'])
def predict_batch():
    """
    Make batch predictions.
    
    Expected JSON input:
    {
        "data": [
            {feature1: value1, feature2: value2, ...},
            {feature1: value1, feature2: value2, ...},
            ...
        ]
    }
    """
    try:
        if model is None:
            return jsonify({
                'error': 'Model not loaded',
                'status': 'error'
            }), 500
            
        data = request.get_json()
        
        if not data or 'data' not in data:
            return jsonify({
                'error': 'No input data provided. Expected {"data": [...]}',
                'status': 'error'
            }), 400
        
        input_list = data['data']
        
        if not isinstance(input_list, list):
            return jsonify({
                'error': 'Input data should be a list',
                'status': 'error'
            }), 400
        
        # Create DataFrame
        input_df = pd.DataFrame(input_list)
        
        # Select only the features used during training
        if feature_names is not None:
            missing_features = set(feature_names) - set(input_df.columns)
            if missing_features:
                return jsonify({
                    'error': f'Missing required features: {list(missing_features)}',
                    'required_features': feature_names.tolist(),
                    'status': 'error'
                }), 400
            
            input_df = input_df[feature_names]
        
        # Scale features if scaler is available
        if scaler is not None:
            input_scaled = scaler.transform(input_df)
        else:
            input_scaled = input_df.values
        
        # Make predictions
        predictions = model.predict(input_scaled)
        
        # Format predictions
        pred_list = []
        for i, pred in enumerate(predictions):
            if isinstance(pred, np.ndarray):
                if pred.ndim > 0 and len(pred) > 1:
                    pred_list.append({
                        'prediction': float(pred[np.argmax(pred)]),
                        'confidence': float(np.max(pred))
                    })
                else:
                    pred_list.append({'prediction': float(pred[0])})
            else:
                pred_list.append({'prediction': float(pred)})
        
        return jsonify({
            'status': 'success',
            'predictions': pred_list,
            'count': len(pred_list),
            'timestamp': datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Batch prediction error: {str(e)}")
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500


@app.route('/model_details', methods=['GET'])
def model_details():
    """Get detailed information about the loaded model."""
    try:
        details = {
            'model_type': type(model).__name__ if model else 'Not loaded',
            'model_path': MODEL_PATH,
            'scaler_loaded': scaler is not None,
            'features_loaded': feature_names is not None,
            'number_of_features': len(feature_names) if feature_names is not None else 0,
            'feature_names': feature_names.tolist() if feature_names is not None else []
        }
        
        # Add model-specific attributes if available
        if hasattr(model, 'feature_importances_'):
            details['has_feature_importances'] = True
        if hasattr(model, 'n_features_in_'):
            details['n_features_in'] = int(model.n_features_in_)
            
        return jsonify(details), 200
        
    except Exception as e:
        logger.error(f"Model details error: {str(e)}")
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        'error': 'Endpoint not found',
        'status': 'error',
        'available_endpoints': {
            '/health': 'GET',
            '/info': 'GET',
            '/model_details': 'GET',
            '/predict': 'POST',
            '/predict_batch': 'POST'
        }
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({
        'error': 'Internal server error',
        'status': 'error'
    }), 500


if __name__ == '__main__':
    # Load model on startup
    try:
        load_model()
        logger.info("Flask application starting...")
        app.run(host='0.0.0.0', port=5000, debug=False)
    except Exception as e:
        logger.error(f"Failed to start application: {str(e)}")
        raise
