"""
Utility functions for the Olympic efficiency analysis project.
"""

import logging
import json
from pathlib import Path


def setup_logging(log_file: str = 'logs/app.log'):
    """
    Setup logging configuration.
    
    Args:
        log_file: Path to log file
    """
    Path(log_file).parent.mkdir(parents=True, exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )


def save_metrics(metrics: dict, output_path: str):
    """
    Save metrics to JSON file.
    
    Args:
        metrics: Dictionary of metrics
        output_path: Path to save JSON file
    """
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(metrics, f, indent=4)


def load_metrics(input_path: str) -> dict:
    """
    Load metrics from JSON file.
    
    Args:
        input_path: Path to JSON file
        
    Returns:
        Dictionary of metrics
    """
    with open(input_path, 'r') as f:
        metrics = json.load(f)
    
    return metrics


def print_metrics(metrics: dict):
    """
    Print metrics in a formatted way.
    
    Args:
        metrics: Dictionary of metrics
    """
    print("\n" + "="*50)
    print("MODEL METRICS")
    print("="*50)
    
    for key, value in metrics.items():
        if isinstance(value, (int, float)):
            print(f"{key:.<30} {value:.4f}")
        else:
            print(f"{key:.<30} {value}")
    
    print("="*50 + "\n")
