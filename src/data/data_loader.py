"""
Data loading and preprocessing module for Olympic efficiency analysis.
"""

import pandas as pd
import numpy as np
import logging
from typing import Tuple, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


def load_data(data_path: str) -> pd.DataFrame:
    """
    Load CSV data from file.
    
    Args:
        data_path: Path to the CSV file
        
    Returns:
        DataFrame containing the loaded data
    """
    try:
        df = pd.read_csv(data_path)
        logger.info(f"Data loaded successfully: {df.shape[0]} rows, {df.shape[1]} columns")
        return df
    except FileNotFoundError:
        logger.error(f"File not found: {data_path}")
        raise
    except Exception as e:
        logger.error(f"Error loading data: {str(e)}")
        raise


def handle_missing_values(df: pd.DataFrame, strategy: str = 'median') -> pd.DataFrame:
    """
    Handle missing values in the dataset.
    
    Args:
        df: Input DataFrame
        strategy: Strategy for handling missing values ('median', 'mean', 'drop')
        
    Returns:
        DataFrame with missing values handled
    """
    df = df.copy()
    
    logger.info(f"Missing values before handling:\n{df.isnull().sum()}")
    
    if strategy == 'median':
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if df[col].isnull().sum() > 0:
                df[col].fillna(df[col].median(), inplace=True)
    elif strategy == 'mean':
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if df[col].isnull().sum() > 0:
                df[col].fillna(df[col].mean(), inplace=True)
    elif strategy == 'drop':
        df.dropna(inplace=True)
    
    logger.info(f"Missing values after handling:\n{df.isnull().sum()}")
    
    return df


def remove_outliers(df: pd.DataFrame, columns: Optional[list] = None, 
                   method: str = 'iqr', threshold: float = 1.5) -> pd.DataFrame:
    """
    Remove outliers from the dataset.
    
    Args:
        df: Input DataFrame
        columns: Columns to check for outliers (None = all numeric)
        method: Method for outlier detection ('iqr' or 'zscore')
        threshold: Threshold for IQR method (1.5 is standard)
        
    Returns:
        DataFrame with outliers removed
    """
    df = df.copy()
    
    if columns is None:
        columns = df.select_dtypes(include=[np.number]).columns.tolist()
    
    initial_shape = df.shape[0]
    
    if method == 'iqr':
        for col in columns:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - threshold * IQR
            upper_bound = Q3 + threshold * IQR
            df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]
    
    elif method == 'zscore':
        from scipy import stats
        z_scores = np.abs(stats.zscore(df[columns]))
        df = df[(z_scores < threshold).all(axis=1)]
    
    removed = initial_shape - df.shape[0]
    logger.info(f"Removed {removed} outliers using {method} method")
    
    return df


def validate_data(df: pd.DataFrame) -> bool:
    """
    Validate data quality.
    
    Args:
        df: DataFrame to validate
        
    Returns:
        True if data is valid, raises exception otherwise
    """
    # Check if dataframe is not empty
    if df.empty:
        raise ValueError("DataFrame is empty")
    
    # Check for necessary columns
    required_cols = ['NOC', 'Year', 'population', 'gdp_per_capita', 'total_medals']
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")
    
    logger.info("Data validation passed")
    return True


def get_data_info(df: pd.DataFrame) -> dict:
    """
    Get informative statistics about the dataset.
    
    Args:
        df: Input DataFrame
        
    Returns:
        Dictionary containing data information
    """
    return {
        'shape': df.shape,
        'columns': df.columns.tolist(),
        'data_types': df.dtypes.to_dict(),
        'missing_values': df.isnull().sum().to_dict(),
        'numeric_summary': df.describe().to_dict(),
        'duplicates': df.duplicated().sum()
    }
