#!/usr/bin/env python3
"""
Example script for making predictions using the trained model.

Usage:
    python predict_example.py --input data.csv --output predictions.csv
"""

import argparse
import pickle
import pandas as pd
import numpy as np
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_model_artifacts(model_path, scaler_path, features_path):
    """Load trained model and preprocessing artifacts."""
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    
    with open(scaler_path, 'rb') as f:
        scaler = pickle.load(f)
    
    with open(features_path, 'rb') as f:
        feature_names = pickle.load(f)
    
    logger.info(f"Loaded model: {type(model).__name__}")
    return model, scaler, feature_names


def make_predictions(model, scaler, feature_names, data_path, output_path):
    """Make predictions on new data."""
    # Load data
    df = pd.read_csv(data_path)
    logger.info(f"Loaded data: {df.shape}")
    
    # Select only required features
    X = df[feature_names]
    
    # Scale features
    X_scaled = scaler.transform(X)
    
    # Make predictions
    predictions = model.predict(X_scaled)
    
    # Save results
    results_df = df.copy()
    results_df['predicted_medals'] = predictions
    results_df.to_csv(output_path, index=False)
    
    logger.info(f"Predictions saved to {output_path}")
    print(f"\nFirst 5 predictions:")
    print(results_df[['NOC', 'Year', 'predicted_medals']].head())


def main():
    parser = argparse.ArgumentParser(description='Make predictions using trained model')
    parser.add_argument('--input', type=str, default='data/processed/test_data.csv',
                       help='Path to input data')
    parser.add_argument('--output', type=str, default='predictions.csv',
                       help='Path to save predictions')
    parser.add_argument('--model', type=str, default='models/best_model.pkl',
                       help='Path to model file')
    parser.add_argument('--scaler', type=str, default='models/scaler.pkl',
                       help='Path to scaler file')
    parser.add_argument('--features', type=str, default='models/feature_names.pkl',
                       help='Path to features file')
    
    args = parser.parse_args()
    
    # Load artifacts
    model, scaler, feature_names = load_model_artifacts(args.model, args.scaler, args.features)
    
    # Make predictions
    make_predictions(model, scaler, feature_names, args.input, args.output)


if __name__ == '__main__':
    main()
