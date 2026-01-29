"""
Visualization module for Olympic efficiency analysis.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)

# Set style
sns.set_style("whitegrid")


def plot_distributions(df: pd.DataFrame, columns: list = None, figsize: tuple = (15, 10)):
    """
    Plot distributions of numerical columns.
    
    Args:
        df: Input DataFrame
        columns: Columns to plot (None = all numeric)
        figsize: Figure size
    """
    if columns is None:
        columns = df.select_dtypes(include=[np.number]).columns.tolist()[:6]
    
    fig, axes = plt.subplots(2, 3, figsize=figsize)
    axes = axes.flatten()
    
    for idx, col in enumerate(columns):
        if idx < len(axes):
            df[col].hist(ax=axes[idx], bins=30, edgecolor='black')
            axes[idx].set_title(f'Distribution of {col}')
            axes[idx].set_xlabel(col)
            axes[idx].set_ylabel('Frequency')
    
    plt.tight_layout()
    logger.info(f"Distribution plots created for {len(columns)} columns")
    return fig


def plot_correlation_heatmap(df: pd.DataFrame, figsize: tuple = (12, 10)):
    """
    Plot correlation heatmap.
    
    Args:
        df: Input DataFrame
        figsize: Figure size
    """
    numeric_df = df.select_dtypes(include=[np.number])
    correlation = numeric_df.corr()
    
    fig, ax = plt.subplots(figsize=figsize)
    sns.heatmap(correlation, annot=True, fmt='.2f', cmap='coolwarm', 
                center=0, ax=ax, cbar_kws={'label': 'Correlation'})
    plt.title('Correlation Heatmap')
    plt.tight_layout()
    
    logger.info("Correlation heatmap created")
    return fig


def plot_predictions_vs_actual(y_test: pd.Series, y_pred: np.ndarray, figsize: tuple = (10, 6)):
    """
    Plot predictions vs actual values.
    
    Args:
        y_test: Actual test values
        y_pred: Predicted values
        figsize: Figure size
    """
    fig, ax = plt.subplots(figsize=figsize)
    ax.scatter(y_test, y_pred, alpha=0.6, edgecolors='k')
    
    # Perfect prediction line
    min_val = min(y_test.min(), y_pred.min())
    max_val = max(y_test.max(), y_pred.max())
    ax.plot([min_val, max_val], [min_val, max_val], 'r--', lw=2, label='Perfect Prediction')
    
    ax.set_xlabel('Actual Values', fontsize=12)
    ax.set_ylabel('Predicted Values', fontsize=12)
    ax.set_title('Predictions vs Actual Values', fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    logger.info("Predictions vs actual plot created")
    return fig


def plot_residuals(y_test: pd.Series, y_pred: np.ndarray, figsize: tuple = (10, 6)):
    """
    Plot residuals.
    
    Args:
        y_test: Actual test values
        y_pred: Predicted values
        figsize: Figure size
    """
    residuals = y_test - y_pred
    
    fig, axes = plt.subplots(1, 2, figsize=figsize)
    
    # Residuals vs Predicted
    axes[0].scatter(y_pred, residuals, alpha=0.6, edgecolors='k')
    axes[0].axhline(y=0, color='r', linestyle='--', lw=2)
    axes[0].set_xlabel('Predicted Values', fontsize=11)
    axes[0].set_ylabel('Residuals', fontsize=11)
    axes[0].set_title('Residuals vs Predicted', fontsize=12, fontweight='bold')
    axes[0].grid(True, alpha=0.3)
    
    # Residuals distribution
    axes[1].hist(residuals, bins=30, edgecolor='black', alpha=0.7)
    axes[1].set_xlabel('Residuals', fontsize=11)
    axes[1].set_ylabel('Frequency', fontsize=11)
    axes[1].set_title('Residuals Distribution', fontsize=12, fontweight='bold')
    axes[1].axvline(x=0, color='r', linestyle='--', lw=2)
    
    plt.tight_layout()
    logger.info("Residual plots created")
    return fig


def plot_feature_importance(model, feature_names: list, top_n: int = 10, figsize: tuple = (10, 6)):
    """
    Plot feature importance.
    
    Args:
        model: Trained model with feature_importances_
        feature_names: List of feature names
        top_n: Number of top features to plot
        figsize: Figure size
    """
    if not hasattr(model, 'feature_importances_'):
        logger.warning("Model does not have feature_importances_ attribute")
        return None
    
    importances = model.feature_importances_
    indices = np.argsort(importances)[::-1][:top_n]
    
    fig, ax = plt.subplots(figsize=figsize)
    ax.bar(range(len(indices)), importances[indices], edgecolor='black', alpha=0.7)
    ax.set_xticks(range(len(indices)))
    ax.set_xticklabels([feature_names[i] for i in indices], rotation=45, ha='right')
    ax.set_ylabel('Importance', fontsize=12)
    ax.set_title(f'Top {top_n} Feature Importances', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    logger.info(f"Feature importance plot created for top {top_n} features")
    return fig


def plot_income_group_analysis(df: pd.DataFrame, figsize: tuple = (14, 8)):
    """
    Plot analysis by income group.
    
    Args:
        df: DataFrame with income_group and medal data
        figsize: Figure size
    """
    fig, axes = plt.subplots(2, 2, figsize=figsize)
    
    if 'income_group' in df.columns and 'total_medals' in df.columns:
        # Boxplot
        df.boxplot(column='total_medals', by='income_group', ax=axes[0, 0])
        axes[0, 0].set_title('Medals by Income Group')
        axes[0, 0].set_xlabel('Income Group')
        axes[0, 0].set_ylabel('Total Medals')
        
        # Count
        income_counts = df['income_group'].value_counts()
        income_counts.plot(kind='bar', ax=axes[0, 1], edgecolor='black')
        axes[0, 1].set_title('Count by Income Group')
        axes[0, 1].set_ylabel('Count')
        axes[0, 1].set_xticklabels(axes[0, 1].get_xticklabels(), rotation=45, ha='right')
    
    if 'gdp_per_capita' in df.columns and 'total_medals' in df.columns:
        # Scatter GDP vs Medals
        for income in df['income_group'].unique():
            subset = df[df['income_group'] == income]
            axes[1, 0].scatter(subset['gdp_per_capita'], subset['total_medals'], 
                             label=income, alpha=0.6, s=50)
        axes[1, 0].set_xlabel('GDP per Capita')
        axes[1, 0].set_ylabel('Total Medals')
        axes[1, 0].set_title('GDP vs Medals by Income Group')
        axes[1, 0].legend()
        axes[1, 0].grid(True, alpha=0.3)
    
    if 'Year' in df.columns and 'total_medals' in df.columns:
        # Trend by year
        yearly_medals = df.groupby('Year')['total_medals'].sum()
        yearly_medals.plot(ax=axes[1, 1], marker='o', edgecolor='black')
        axes[1, 1].set_xlabel('Year')
        axes[1, 1].set_ylabel('Total Medals')
        axes[1, 1].set_title('Total Medals Trend by Year')
        axes[1, 1].grid(True, alpha=0.3)
    
    plt.suptitle('')  # Remove automatic title
    plt.tight_layout()
    logger.info("Income group analysis plots created")
    return fig
