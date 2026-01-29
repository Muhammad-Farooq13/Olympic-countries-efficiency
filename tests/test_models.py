"""
Unit tests for model training and evaluation.
"""

import unittest
import numpy as np
import pandas as pd
from pathlib import Path

# Add src to path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.models.train import create_model, prepare_data, evaluate_model


class TestModelCreation(unittest.TestCase):
    """Test model creation functionality."""
    
    def test_create_linear_model(self):
        """Test creating linear regression model."""
        model = create_model('linear')
        
        self.assertIsNotNone(model)
        self.assertEqual(type(model).__name__, 'LinearRegression')
    
    def test_create_rf_model(self):
        """Test creating random forest model."""
        model = create_model('rf', n_estimators=10)
        
        self.assertIsNotNone(model)
        self.assertEqual(type(model).__name__, 'RandomForestRegressor')
    
    def test_create_ridge_model(self):
        """Test creating ridge regression model."""
        model = create_model('ridge', alpha=0.5)
        
        self.assertIsNotNone(model)
        self.assertEqual(type(model).__name__, 'Ridge')


class TestDataPreparation(unittest.TestCase):
    """Test data preparation for modeling."""
    
    def setUp(self):
        """Set up test fixtures."""
        np.random.seed(42)
        self.X = pd.DataFrame({
            'feature1': np.random.rand(100),
            'feature2': np.random.rand(100),
            'feature3': np.random.rand(100)
        })
        self.y = pd.Series(np.random.rand(100))
    
    def test_prepare_data_shapes(self):
        """Test that data preparation produces correct shapes."""
        X_train, X_test, y_train, y_test, scaler, features = prepare_data(
            self.X, self.y, test_size=0.2
        )
        
        self.assertEqual(X_train.shape[0], 80)
        self.assertEqual(X_test.shape[0], 20)
        self.assertEqual(len(features), 3)
    
    def test_scaler_fitting(self):
        """Test that scaler is properly fitted."""
        X_train, X_test, y_train, y_test, scaler, features = prepare_data(
            self.X, self.y
        )
        
        # Check that scaler has been fitted
        self.assertIsNotNone(scaler.mean_)
        self.assertIsNotNone(scaler.scale_)


class TestModelEvaluation(unittest.TestCase):
    """Test model evaluation functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        from sklearn.ensemble import RandomForestRegressor
        
        np.random.seed(42)
        self.X_train = np.random.rand(80, 3)
        self.X_test = np.random.rand(20, 3)
        self.y_train = np.random.rand(80)
        self.y_test = np.random.rand(20)
        
        self.model = RandomForestRegressor(n_estimators=5, random_state=42)
        self.model.fit(self.X_train, self.y_train)
    
    def test_evaluate_model_metrics(self):
        """Test that evaluation produces expected metrics."""
        metrics = evaluate_model(self.model, self.X_test, pd.Series(self.y_test))
        
        self.assertIn('r2_score', metrics)
        self.assertIn('rmse', metrics)
        self.assertIn('mae', metrics)
        self.assertIn('mape', metrics)
    
    def test_metrics_are_numeric(self):
        """Test that all metrics are numeric values."""
        metrics = evaluate_model(self.model, self.X_test, pd.Series(self.y_test))
        
        for value in metrics.values():
            self.assertTrue(isinstance(value, (int, float, np.number)))


if __name__ == '__main__':
    unittest.main()
