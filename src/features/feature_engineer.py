"""
Feature engineering module for Olympic efficiency analysis.
"""

import pandas as pd
import numpy as np
import logging
from typing import List, Tuple

logger = logging.getLogger(__name__)


def create_ratio_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create ratio-based features from existing columns.
    
    Args:
        df: Input DataFrame
        
    Returns:
        DataFrame with new ratio features
    """
    df = df.copy()
    
    # Athletes per capita
    if 'athletes_sent' in df.columns and 'population' in df.columns:
        df['athletes_per_capita'] = df['athletes_sent'] / (df['population'] + 1e-6)
        logger.info("Created athletes_per_capita feature")
    
    # Events per sport
    if 'events_participated' in df.columns and 'sports_participated' in df.columns:
        df['events_per_sport'] = df['events_participated'] / (df['sports_participated'] + 1e-6)
        logger.info("Created events_per_sport feature")
    
    # Medals per athlete
    if 'total_medals' in df.columns and 'athletes_sent' in df.columns:
        df['medals_per_athlete'] = df['total_medals'] / (df['athletes_sent'] + 1e-6)
        logger.info("Created medals_per_athlete feature")
    
    # GDP weighted medals
    if 'total_medals' in df.columns and 'gdp_per_capita' in df.columns:
        df['medals_per_gdp'] = df['total_medals'] / (df['gdp_per_capita'] + 1)
        logger.info("Created medals_per_gdp feature")
    
    return df


def create_temporal_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create temporal features from year column.
    
    Args:
        df: Input DataFrame with 'Year' column
        
    Returns:
        DataFrame with new temporal features
    """
    df = df.copy()
    
    if 'Year' in df.columns:
        # Years since first record
        df['years_since_first'] = df['Year'] - df['Year'].min()
        
        # Olympic cycle (every 4 years)
        df['olympic_cycle'] = (df['Year'] - df['Year'].min()) // 4
        
        logger.info("Created temporal features")
    
    return df


def create_performance_categories(df: pd.DataFrame, 
                                  medal_bins: List[int] = [0, 1, 5, 10, 100]) -> pd.DataFrame:
    """
    Create categorical features for performance levels.
    
    Args:
        df: Input DataFrame
        medal_bins: Bins for medal categorization
        
    Returns:
        DataFrame with performance categories
    """
    df = df.copy()
    
    if 'total_medals' in df.columns:
        labels = ['No medals', 'Few medals', 'Some medals', 'Many medals', 'Very many medals']
        df['medal_performance'] = pd.cut(df['total_medals'], bins=medal_bins, labels=labels[:len(medal_bins)-1])
        logger.info("Created medal_performance category")
    
    return df


def encode_categorical(df: pd.DataFrame, columns: List[str] = None) -> pd.DataFrame:
    """
    One-hot encode categorical variables.
    
    Args:
        df: Input DataFrame
        columns: Columns to encode (None = all object/category types)
        
    Returns:
        DataFrame with encoded categorical variables
    """
    df = df.copy()
    
    if columns is None:
        columns = df.select_dtypes(include=['object']).columns.tolist()
    
    # Filter to only existing columns
    columns = [col for col in columns if col in df.columns]
    
    if columns:
        df = pd.get_dummies(df, columns=columns, drop_first=True)
        logger.info(f"Encoded categorical columns: {columns}")
    
    return df


def normalize_features(df: pd.DataFrame, columns: List[str] = None) -> pd.DataFrame:
    """
    Normalize numerical features to 0-1 range.
    
    Args:
        df: Input DataFrame
        columns: Columns to normalize (None = all numeric)
        
    Returns:
        Normalized DataFrame
    """
    df = df.copy()
    
    if columns is None:
        columns = df.select_dtypes(include=[np.number]).columns.tolist()
    
    for col in columns:
        if col in df.columns:
            min_val = df[col].min()
            max_val = df[col].max()
            if max_val > min_val:
                df[col] = (df[col] - min_val) / (max_val - min_val)
    
    logger.info(f"Normalized {len(columns)} features")
    
    return df


def create_interaction_features(df: pd.DataFrame, feature_pairs: List[Tuple] = None) -> pd.DataFrame:
    """
    Create interaction features.
    
    Args:
        df: Input DataFrame
        feature_pairs: List of tuples for feature pairs to multiply
        
    Returns:
        DataFrame with interaction features
    """
    df = df.copy()
    
    if feature_pairs is None:
        feature_pairs = [
            ('population', 'gdp_per_capita'),
            ('athletes_sent', 'female_athlete_percentage'),
            ('sports_participated', 'events_participated')
        ]
    
    for feat1, feat2 in feature_pairs:
        if feat1 in df.columns and feat2 in df.columns:
            df[f'{feat1}_{feat2}_interaction'] = df[feat1] * df[feat2]
            logger.info(f"Created interaction feature: {feat1}_{feat2}_interaction")
    
    return df


def engineer_features(df: pd.DataFrame, config: dict = None) -> pd.DataFrame:
    """
    Apply all feature engineering transformations.
    
    Args:
        df: Input DataFrame
        config: Configuration dictionary
        
    Returns:
        DataFrame with engineered features
    """
    df = df.copy()
    
    logger.info("Starting feature engineering...")
    
    # Apply transformations
    df = create_ratio_features(df)
    df = create_temporal_features(df)
    df = create_performance_categories(df)
    df = create_interaction_features(df)
    df = encode_categorical(df, columns=['income_group'])
    
    logger.info(f"Feature engineering completed. Total features: {df.shape[1]}")
    
    return df
