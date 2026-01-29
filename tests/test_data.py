"""
Unit tests for data loading and preprocessing.
"""

import unittest
import pandas as pd
import numpy as np
from pathlib import Path

# Add src to path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.data.data_loader import load_data, handle_missing_values, remove_outliers


class TestDataLoading(unittest.TestCase):
    """Test data loading functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_data = pd.DataFrame({
            'A': [1, 2, 3, 4, 5],
            'B': [5, 4, 3, 2, 1],
            'C': [1.1, 2.2, 3.3, 4.4, 5.5]
        })
    
    def test_handle_missing_values_median(self):
        """Test missing value handling with median strategy."""
        df = self.test_data.copy()
        df.loc[0, 'A'] = np.nan
        
        result = handle_missing_values(df, strategy='median')
        
        self.assertFalse(result['A'].isnull().any())
        self.assertEqual(result.loc[0, 'A'], 3.0)  # Median of [2,3,4,5]
    
    def test_remove_outliers_iqr(self):
        """Test outlier removal using IQR method."""
        df = self.test_data.copy()
        df.loc[5] = [100, -100, 100.0]  # Add outliers
        
        result = remove_outliers(df, columns=['A'], method='iqr')
        
        self.assertLess(result.shape[0], df.shape[0])
    
    def test_remove_duplicates(self):
        """Test removing duplicates."""
        df = pd.concat([self.test_data, self.test_data], ignore_index=True)
        
        df_clean = df.drop_duplicates()
        
        self.assertEqual(df_clean.shape[0], self.test_data.shape[0])


class TestDataValidation(unittest.TestCase):
    """Test data validation."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.valid_data = pd.DataFrame({
            'NOC': ['USA', 'CHN', 'JPN'],
            'Year': [2020, 2020, 2020],
            'population': [330e6, 1400e6, 125e6],
            'gdp_per_capita': [60000, 10000, 40000],
            'total_medals': [113, 88, 58]
        })
    
    def test_valid_data(self):
        """Test that valid data passes validation."""
        from src.data.data_loader import validate_data
        
        self.assertTrue(validate_data(self.valid_data))


if __name__ == '__main__':
    unittest.main()
