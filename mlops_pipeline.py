"""
MLOps Pipeline for Olympic Countries Efficiency Project.

This script orchestrates the entire ML workflow:
1. Data loading and validation
2. Feature engineering
3. Model training and evaluation
4. Model versioning and logging
5. Artifact storage

Usage:
    python mlops_pipeline.py --config config/pipeline_config.yaml --mode train
    python mlops_pipeline.py --config config/pipeline_config.yaml --mode evaluate
"""

import os
import sys
import json
import yaml
import pickle
import logging
import argparse
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.linear_model import LinearRegression, Ridge, Lasso

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/mlops_pipeline.log', mode='a'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Create logs directory if it doesn't exist
Path('logs').mkdir(exist_ok=True)


class MLOpsPipeline:
    """Main MLOps Pipeline class."""
    
    def __init__(self, config_path: str = None):
        """Initialize the pipeline with configuration."""
        self.config = self._load_config(config_path)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.run_id = f"run_{self.timestamp}"
        
        # Create output directories
        self._create_directories()
        
        logger.info(f"MLOps Pipeline initialized with run_id: {self.run_id}")
    
    def _load_config(self, config_path: str) -> dict:
        """Load configuration from file or use defaults."""
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            logger.info(f"Configuration loaded from {config_path}")
        else:
            config = self._get_default_config()
            logger.info("Using default configuration")
        
        return config
    
    @staticmethod
    def _get_default_config() -> dict:
        """Return default configuration."""
        return {
            'data': {
                'raw_path': 'data/raw/olympic_countries_efficiency.csv',
                'processed_path': 'data/processed/processed_data.csv',
                'train_size': 0.8,
                'test_size': 0.2,
                'random_state': 42,
                'target_column': 'total_medals'
            },
            'preprocessing': {
                'handle_missing': True,
                'scale_features': True,
                'outlier_method': 'iqr'  # 'iqr' or 'zscore'
            },
            'model': {
                'type': 'xgboost',  # 'linear', 'rf', 'xgboost', 'gb'
                'random_state': 42,
                'hyperparameters': {
                    'n_estimators': 100,
                    'max_depth': 5,
                    'learning_rate': 0.1
                }
            },
            'training': {
                'cross_val_folds': 5,
                'hyperparameter_tuning': False,
                'save_model': True,
                'save_plots': True
            }
        }
    
    def _create_directories(self):
        """Create necessary output directories."""
        directories = [
            'logs',
            'data/raw',
            'data/processed',
            'models',
            'outputs/plots',
            'outputs/reports',
            'outputs/metrics'
        ]
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
    
    def load_data(self) -> pd.DataFrame:
        """Load raw data."""
        data_path = self.config['data']['raw_path']
        
        try:
            df = pd.read_csv(data_path)
            logger.info(f"Data loaded: {df.shape[0]} rows, {df.shape[1]} columns")
            
            # Log data info
            logger.info(f"Data columns: {list(df.columns)}")
            logger.info(f"Data types:\n{df.dtypes}")
            logger.info(f"Missing values:\n{df.isnull().sum()}")
            
            return df
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            raise
    
    def preprocess_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Preprocess and clean data."""
        logger.info("Starting data preprocessing...")
        
        df = df.copy()
        
        # Handle missing values
        if self.config['preprocessing']['handle_missing']:
            logger.info(f"Missing values before imputation:\n{df.isnull().sum()}")
            
            # Fill numeric columns with median
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            for col in numeric_cols:
                if df[col].isnull().sum() > 0:
                    df[col].fillna(df[col].median(), inplace=True)
            
            # Drop rows with missing categorical values
            df.dropna(inplace=True)
            
            logger.info(f"Missing values after imputation:\n{df.isnull().sum()}")
        
        # Remove duplicates
        initial_shape = df.shape[0]
        df.drop_duplicates(inplace=True)
        logger.info(f"Removed {initial_shape - df.shape[0]} duplicate rows")
        
        logger.info(f"Data shape after preprocessing: {df.shape}")
        
        return df
    
    def feature_engineering(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create new features."""
        logger.info("Starting feature engineering...")
        
        df = df.copy()
        
        # Create ratio features
        if 'athletes_sent' in df.columns and 'population' in df.columns:
            df['athletes_per_capita'] = df['athletes_sent'] / (df['population'] + 1e-6)
            logger.info("Created athletes_per_capita feature")
        
        if 'events_participated' in df.columns and 'sports_participated' in df.columns:
            df['events_per_sport'] = df['events_participated'] / (df['sports_participated'] + 1e-6)
            logger.info("Created events_per_sport feature")
        
        if 'total_medals' in df.columns and 'athletes_sent' in df.columns:
            df['medals_per_athlete'] = df['total_medals'] / (df['athletes_sent'] + 1e-6)
            logger.info("Created medals_per_athlete feature")
        
        # Encode categorical variables
        if 'income_group' in df.columns:
            df = pd.get_dummies(df, columns=['income_group'], drop_first=True)
            logger.info("Encoded income_group categorical variable")
        
        logger.info(f"Features after engineering: {list(df.columns)}")
        
        return df
    
    def prepare_train_test(self, df: pd.DataFrame):
        """Prepare training and test sets."""
        logger.info("Preparing train and test sets...")
        
        target_col = self.config['data']['target_column']
        
        if target_col not in df.columns:
            logger.error(f"Target column '{target_col}' not found in data")
            raise ValueError(f"Target column '{target_col}' not found")
        
        # Separate features and target
        X = df.drop(columns=[target_col])
        y = df[target_col]
        
        # Remove categorical columns that aren't encoded
        categorical_cols = X.select_dtypes(include=['object']).columns
        if len(categorical_cols) > 0:
            logger.warning(f"Dropping categorical columns: {list(categorical_cols)}")
            X = X.drop(columns=categorical_cols)
        
        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y,
            test_size=self.config['data']['test_size'],
            random_state=self.config['data']['random_state']
        )
        
        logger.info(f"Train set shape: {X_train.shape}, Test set shape: {X_test.shape}")
        
        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        logger.info("Features scaled using StandardScaler")
        
        return X_train_scaled, X_test_scaled, y_train, y_test, scaler, X.columns.tolist()
    
    def train_model(self, X_train, y_train, X_test, y_test):
        """Train the model."""
        logger.info("Starting model training...")
        
        model_type = self.config['model']['type']
        random_state = self.config['model']['random_state']
        
        # Initialize model based on configuration
        if model_type == 'linear':
            model = LinearRegression()
        elif model_type == 'ridge':
            model = Ridge(random_state=random_state)
        elif model_type == 'lasso':
            model = Lasso(random_state=random_state)
        elif model_type == 'rf':
            model = RandomForestRegressor(
                n_estimators=self.config['model']['hyperparameters'].get('n_estimators', 100),
                random_state=random_state,
                n_jobs=-1
            )
        elif model_type == 'gb':
            model = GradientBoostingRegressor(
                n_estimators=self.config['model']['hyperparameters'].get('n_estimators', 100),
                random_state=random_state
            )
        else:
            logger.warning(f"Unknown model type {model_type}, using Linear Regression")
            model = LinearRegression()
        
        # Train model
        model.fit(X_train, y_train)
        logger.info(f"Model trained: {type(model).__name__}")
        
        # Cross-validation
        cv_scores = cross_val_score(
            model, X_train, y_train,
            cv=self.config['training']['cross_val_folds'],
            scoring='r2'
        )
        logger.info(f"Cross-validation scores: mean={cv_scores.mean():.4f}, std={cv_scores.std():.4f}")
        
        # Evaluate on test set
        y_pred = model.predict(X_test)
        
        metrics = {
            'r2_score': r2_score(y_test, y_pred),
            'rmse': np.sqrt(mean_squared_error(y_test, y_pred)),
            'mae': mean_absolute_error(y_test, y_pred),
            'cv_mean': cv_scores.mean(),
            'cv_std': cv_scores.std()
        }
        
        for metric_name, metric_value in metrics.items():
            logger.info(f"{metric_name}: {metric_value:.4f}")
        
        return model, metrics, y_pred
    
    def save_artifacts(self, model, scaler, feature_names, metrics, y_test, y_pred):
        """Save model and artifacts."""
        logger.info("Saving artifacts...")
        
        # Save model
        model_path = f"models/model_{self.run_id}.pkl"
        with open(model_path, 'wb') as f:
            pickle.dump(model, f)
        logger.info(f"Model saved to {model_path}")
        
        # Save scaler
        scaler_path = f"models/scaler_{self.run_id}.pkl"
        with open(scaler_path, 'wb') as f:
            pickle.dump(scaler, f)
        logger.info(f"Scaler saved to {scaler_path}")
        
        # Save feature names
        features_path = f"models/feature_names_{self.run_id}.pkl"
        with open(features_path, 'wb') as f:
            pickle.dump(feature_names, f)
        logger.info(f"Feature names saved to {features_path}")
        
        # Save metrics
        metrics_path = f"outputs/metrics/metrics_{self.run_id}.json"
        with open(metrics_path, 'w') as f:
            json.dump(metrics, f, indent=4)
        logger.info(f"Metrics saved to {metrics_path}")
        
        # Create links to latest models (for easy reference)
        import shutil
        for src, link_name in [
            (model_path, 'models/best_model.pkl'),
            (scaler_path, 'models/scaler.pkl'),
            (features_path, 'models/feature_names.pkl')
        ]:
            try:
                if os.path.exists(link_name):
                    os.remove(link_name)
                shutil.copy(src, link_name)
                logger.info(f"Updated link: {link_name}")
            except Exception as e:
                logger.warning(f"Could not update link {link_name}: {str(e)}")
        
        return {
            'model_path': model_path,
            'scaler_path': scaler_path,
            'features_path': features_path,
            'metrics_path': metrics_path
        }
    
    def create_visualizations(self, y_test, y_pred, model, feature_names):
        """Create and save visualizations."""
        logger.info("Creating visualizations...")
        
        # Predictions vs Actuals
        plt.figure(figsize=(10, 6))
        plt.scatter(y_test, y_pred, alpha=0.5)
        plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
        plt.xlabel('Actual Values')
        plt.ylabel('Predicted Values')
        plt.title('Predictions vs Actual Values')
        plt.tight_layout()
        plot_path = f"outputs/plots/predictions_vs_actual_{self.run_id}.png"
        plt.savefig(plot_path, dpi=300, bbox_inches='tight')
        logger.info(f"Saved plot: {plot_path}")
        plt.close()
        
        # Residuals
        residuals = y_test - y_pred
        plt.figure(figsize=(10, 6))
        plt.scatter(y_pred, residuals, alpha=0.5)
        plt.axhline(y=0, color='r', linestyle='--', lw=2)
        plt.xlabel('Predicted Values')
        plt.ylabel('Residuals')
        plt.title('Residual Plot')
        plt.tight_layout()
        plot_path = f"outputs/plots/residuals_{self.run_id}.png"
        plt.savefig(plot_path, dpi=300, bbox_inches='tight')
        logger.info(f"Saved plot: {plot_path}")
        plt.close()
        
        # Feature importance (if available)
        if hasattr(model, 'feature_importances_'):
            importances = model.feature_importances_
            indices = np.argsort(importances)[::-1][:10]  # Top 10
            
            plt.figure(figsize=(10, 6))
            plt.title('Top 10 Feature Importances')
            plt.bar(range(len(indices)), importances[indices])
            plt.xticks(range(len(indices)), [feature_names[i] for i in indices], rotation=45)
            plt.tight_layout()
            plot_path = f"outputs/plots/feature_importance_{self.run_id}.png"
            plt.savefig(plot_path, dpi=300, bbox_inches='tight')
            logger.info(f"Saved plot: {plot_path}")
            plt.close()
    
    def run_pipeline(self, mode: str = 'train'):
        """Execute the complete pipeline."""
        try:
            logger.info(f"Starting MLOps Pipeline in '{mode}' mode")
            
            # Load data
            df = self.load_data()
            
            # Preprocess
            df = self.preprocess_data(df)
            
            # Feature engineering
            df = self.feature_engineering(df)
            
            # Save processed data
            processed_path = self.config['data']['processed_path']
            df.to_csv(processed_path, index=False)
            logger.info(f"Processed data saved to {processed_path}")
            
            # Prepare train-test sets
            X_train, X_test, y_train, y_test, scaler, feature_names = self.prepare_train_test(df)
            
            # Train model
            model, metrics, y_pred = self.train_model(X_train, y_train, X_test, y_test)
            
            # Save artifacts
            artifact_paths = self.save_artifacts(model, scaler, feature_names, metrics, y_test, y_pred)
            
            # Create visualizations
            if self.config['training'].get('save_plots', True):
                self.create_visualizations(y_test, y_pred, model, feature_names)
            
            logger.info("MLOps Pipeline completed successfully!")
            
            return {
                'status': 'success',
                'run_id': self.run_id,
                'metrics': metrics,
                'artifacts': artifact_paths
            }
            
        except Exception as e:
            logger.error(f"Pipeline failed: {str(e)}", exc_info=True)
            raise


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='MLOps Pipeline for Olympic Efficiency Analysis')
    parser.add_argument('--config', type=str, help='Path to configuration file')
    parser.add_argument('--mode', type=str, choices=['train', 'evaluate'], default='train',
                       help='Pipeline mode')
    
    args = parser.parse_args()
    
    pipeline = MLOpsPipeline(config_path=args.config)
    result = pipeline.run_pipeline(mode=args.mode)
    
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
