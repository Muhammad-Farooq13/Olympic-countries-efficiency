"""
Model training and evaluation module.
"""

import numpy as np
import pandas as pd
import logging
import pickle
from typing import Tuple, Dict, Any
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

logger = logging.getLogger(__name__)


def prepare_data(X: pd.DataFrame, y: pd.Series, 
                test_size: float = 0.2, random_state: int = 42
                ) -> Tuple[np.ndarray, np.ndarray, pd.Series, pd.Series, StandardScaler, list]:
    """
    Prepare and scale data for modeling.
    
    Args:
        X: Features DataFrame
        y: Target Series
        test_size: Proportion of data for testing
        random_state: Random seed
        
    Returns:
        Tuple of (X_train_scaled, X_test_scaled, y_train, y_test, scaler, feature_names)
    """
    # Remove non-numeric columns
    numeric_cols = X.select_dtypes(include=[np.number]).columns.tolist()
    X = X[numeric_cols]
    
    feature_names = X.columns.tolist()
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    logger.info(f"Data prepared: train shape {X_train_scaled.shape}, test shape {X_test_scaled.shape}")
    
    return X_train_scaled, X_test_scaled, y_train, y_test, scaler, feature_names


def create_model(model_type: str, **kwargs) -> Any:
    """
    Create a machine learning model.
    
    Args:
        model_type: Type of model ('linear', 'ridge', 'lasso', 'rf', 'gb')
        **kwargs: Additional arguments for model
        
    Returns:
        Initialized model
    """
    if model_type == 'linear':
        model = LinearRegression()
    elif model_type == 'ridge':
        model = Ridge(alpha=kwargs.get('alpha', 1.0), random_state=kwargs.get('random_state', 42))
    elif model_type == 'lasso':
        model = Lasso(alpha=kwargs.get('alpha', 1.0), random_state=kwargs.get('random_state', 42))
    elif model_type == 'rf':
        model = RandomForestRegressor(
            n_estimators=kwargs.get('n_estimators', 100),
            max_depth=kwargs.get('max_depth', None),
            random_state=kwargs.get('random_state', 42),
            n_jobs=-1
        )
    elif model_type == 'gb':
        model = GradientBoostingRegressor(
            n_estimators=kwargs.get('n_estimators', 100),
            learning_rate=kwargs.get('learning_rate', 0.1),
            max_depth=kwargs.get('max_depth', 3),
            random_state=kwargs.get('random_state', 42)
        )
    else:
        logger.warning(f"Unknown model type {model_type}, using Linear Regression")
        model = LinearRegression()
    
    logger.info(f"Model created: {type(model).__name__}")
    return model


def train_model(model: Any, X_train: np.ndarray, y_train: pd.Series) -> Any:
    """
    Train a model.
    
    Args:
        model: Model to train
        X_train: Training features
        y_train: Training target
        
    Returns:
        Trained model
    """
    model.fit(X_train, y_train)
    logger.info(f"Model trained: {type(model).__name__}")
    return model


def evaluate_model(model: Any, X_test: np.ndarray, y_test: pd.Series) -> Dict[str, float]:
    """
    Evaluate model performance.
    
    Args:
        model: Trained model
        X_test: Test features
        y_test: Test target
        
    Returns:
        Dictionary of evaluation metrics
    """
    y_pred = model.predict(X_test)
    
    metrics = {
        'r2_score': r2_score(y_test, y_pred),
        'rmse': np.sqrt(mean_squared_error(y_test, y_pred)),
        'mae': mean_absolute_error(y_test, y_pred),
        'mape': np.mean(np.abs((y_test - y_pred) / (y_test + 1e-6))) * 100
    }
    
    logger.info(f"Model evaluation: {metrics}")
    
    return metrics


def cross_validate_model(model: Any, X_train: np.ndarray, y_train: pd.Series,
                        cv: int = 5) -> Dict[str, float]:
    """
    Perform cross-validation.
    
    Args:
        model: Model to validate
        X_train: Training features
        y_train: Training target
        cv: Number of folds
        
    Returns:
        Dictionary of CV results
    """
    scores = cross_val_score(model, X_train, y_train, cv=cv, scoring='r2')
    
    results = {
        'cv_mean': scores.mean(),
        'cv_std': scores.std(),
        'cv_scores': scores.tolist()
    }
    
    logger.info(f"Cross-validation results: mean={scores.mean():.4f}, std={scores.std():.4f}")
    
    return results


def hyperparameter_tuning(model_type: str, X_train: np.ndarray, y_train: pd.Series,
                         param_grid: Dict[str, list], cv: int = 5) -> Tuple[Any, Dict]:
    """
    Perform hyperparameter tuning using grid search.
    
    Args:
        model_type: Type of model
        X_train: Training features
        y_train: Training target
        param_grid: Parameter grid for search
        cv: Number of CV folds
        
    Returns:
        Tuple of (best_model, best_params)
    """
    base_model = create_model(model_type)
    
    grid_search = GridSearchCV(base_model, param_grid, cv=cv, scoring='r2', n_jobs=-1)
    grid_search.fit(X_train, y_train)
    
    logger.info(f"Best parameters: {grid_search.best_params_}")
    logger.info(f"Best CV score: {grid_search.best_score_:.4f}")
    
    return grid_search.best_estimator_, grid_search.best_params_


def save_model(model: Any, scaler: StandardScaler, feature_names: list, 
              model_path: str, scaler_path: str, features_path: str):
    """
    Save model, scaler, and feature names.
    
    Args:
        model: Trained model
        scaler: Fitted scaler
        feature_names: List of feature names
        model_path: Path to save model
        scaler_path: Path to save scaler
        features_path: Path to save feature names
    """
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    logger.info(f"Model saved to {model_path}")
    
    with open(scaler_path, 'wb') as f:
        pickle.dump(scaler, f)
    logger.info(f"Scaler saved to {scaler_path}")
    
    with open(features_path, 'wb') as f:
        pickle.dump(feature_names, f)
    logger.info(f"Feature names saved to {features_path}")


def load_model(model_path: str, scaler_path: str, features_path: str):
    """
    Load model, scaler, and feature names.
    
    Args:
        model_path: Path to model file
        scaler_path: Path to scaler file
        features_path: Path to features file
        
    Returns:
        Tuple of (model, scaler, feature_names)
    """
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    
    with open(scaler_path, 'rb') as f:
        scaler = pickle.load(f)
    
    with open(features_path, 'rb') as f:
        feature_names = pickle.load(f)
    
    logger.info(f"Model loaded from {model_path}")
    
    return model, scaler, feature_names
