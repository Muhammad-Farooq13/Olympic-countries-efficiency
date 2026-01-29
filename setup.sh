#!/bin/bash
# Project Setup Script for Unix/Linux/Mac

set -e

echo "========================================="
echo "Olympic Efficiency Analysis - Setup"
echo "========================================="

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Install package in development mode
echo "Installing package..."
pip install -e .

# Create necessary directories
echo "Creating directories..."
mkdir -p data/raw data/processed notebooks logs models outputs/plots outputs/reports outputs/metrics

# Copy raw data if needed
if [ ! -f "data/raw/olympic_countries_efficiency.csv" ]; then
    echo "Warning: Raw data not found. Please add olympic_countries_efficiency.csv to data/raw/"
fi

echo ""
echo "========================================="
echo "Setup Complete!"
echo "========================================="
echo ""
echo "Next steps:"
echo "1. Activate environment: source venv/bin/activate"
echo "2. Run pipeline: python mlops_pipeline.py"
echo "3. Start Flask: python flask_app.py"
echo "4. Run tests: pytest tests/"
echo ""
