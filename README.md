# Olympic Countries Efficiency Analysis

## Project Overview

This project analyzes Olympic participation and performance efficiency across countries, examining the relationship between socioeconomic factors (population, GDP per capita) and medal performance. The goal is to build predictive models that can estimate a country's Olympic medal performance based on their socioeconomic indicators and participation metrics.

## Business Objective

- **Primary Goal**: Predict total medals and medals per athlete based on country characteristics
- **Secondary Goals**: 
  - Analyze efficiency patterns across income groups
  - Identify factors influencing athletic performance
  - Compare performance trends across Olympic years
  - Provide insights for sports development planning

## Dataset Overview

### Source
Olympic countries efficiency dataset containing performance metrics from 1992-2016 Summer Olympics.

### Features
- **Country Information**: NOC (National Olympic Committee), ISO3 code, Year
- **Socioeconomic Indicators**: Population, GDP per capita, Income group classification
- **Participation Metrics**: Athletes sent, sports participated, events participated
- **Performance Data**: Gold/Silver/Bronze medals, total medals, medals per athlete
- **Demographics**: Female athlete percentage
- **Historical Data**: Previous total medals, previous medals per athlete
- **Context**: Host country indicator

### Data Characteristics
- **Records**: 250+ Olympic participation records
- **Time Period**: 1992-2016 Summer Olympics
- **Income Groups**: Low income, Lower-middle income, Upper-middle income, High income
- **Missing Values**: Some countries have no medal performance (zeros are valid)

### Preprocessing Steps
1. **Handling Missing Values**: Fill NaN values appropriately based on context
2. **Feature Scaling**: Standardize numerical features for model training
3. **Categorical Encoding**: One-hot encode income groups
4. **Outlier Detection**: Identify and handle extreme values
5. **Train-Test Split**: Temporal split respecting data collection order

## Project Structure

```
olympic_countries_efficiency/
├── data/
│   ├── raw/                 # Original raw dataset
│   └── processed/           # Cleaned and processed data
├── notebooks/
│   ├── 01_eda.ipynb        # Exploratory data analysis
│   ├── 02_preprocessing.ipynb # Data preprocessing
│   ├── 03_feature_engineering.ipynb # Feature creation
│   ├── 04_model_development.ipynb # Model development
│   └── 05_evaluation.ipynb  # Model evaluation and validation
├── src/
│   ├── data/               # Data loading and preprocessing modules
│   ├── features/           # Feature engineering modules
│   ├── models/             # Model training and evaluation
│   ├── visualization/      # Plotting and visualization functions
│   └── utils/              # Utility functions
├── tests/                  # Unit tests
├── models/                 # Saved model artifacts
├── requirements.txt        # Python dependencies
├── setup.py               # Package setup configuration
├── Dockerfile             # Docker containerization
├── flask_app.py           # Flask application for model serving
├── mlops_pipeline.py      # MLOps pipeline configuration
├── .gitignore             # Git ignore file
└── LICENSE                # License file
```

## Methodology

### 1. Exploratory Data Analysis (EDA)
- Statistical summaries and distributions
- Correlation analysis between features and target
- Visualization of trends and patterns
- Missing value analysis

### 2. Data Preprocessing
- Data validation and cleaning
- Handling missing values through imputation or removal
- Outlier detection and treatment
- Feature normalization and scaling

### 3. Feature Engineering
- Creating interaction features (e.g., athletes per capita)
- Temporal features from Olympic year
- Efficiency metrics and ratios
- Polynomial and derived features

### 4. Model Development
- **Regression Models**: Predicting continuous medal performance
  - Linear Regression (baseline)
  - Ridge/Lasso Regression (regularization)
  - Random Forest Regression
  - Gradient Boosting (XGBoost)
  - Neural Networks (Deep Learning)
  
- **Classification Models**: Predicting medal performance categories
  - Logistic Regression
  - Random Forest Classifier
  - XGBoost Classifier
  - Neural Networks

### 5. Model Evaluation
- **Metrics**: RMSE, MAE, R² for regression; Accuracy, Precision, Recall, F1 for classification
- **Cross-validation**: K-fold cross-validation for robustness
- **Hyperparameter Tuning**: Grid search and random search
- **Model Comparison**: Evaluation across multiple metrics

### 6. Deployment
- Flask API for model serving
- Docker containerization for reproducibility
- MLOps pipeline for continuous integration/deployment

## Installation and Setup

### Prerequisites
- Python 3.8 or higher
- pip or conda package manager
- Docker (for containerized deployment)
- Git (for version control)

### Local Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Muhammad-Farooq-13/olympic-countries-efficiency.git
   cd olympic-countries-efficiency
   ```

2. **Create a virtual environment**
   ```bash
   # Using venv
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Or using conda
   conda create -n olympic python=3.9
   conda activate olympic
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the project**
   ```bash
   pip install -e .
   ```

## Usage

### Running Exploratory Data Analysis
```bash
jupyter notebook notebooks/01_eda.ipynb
```

### Running the Complete Pipeline
```bash
python mlops_pipeline.py
```

### Training Models
```bash
python src/models/train.py --config config/model_config.yaml
```

### Making Predictions
```bash
python src/models/predict.py --model models/best_model.pkl --input data/processed/test_data.csv
```

### Starting the Flask Application

**Locally:**
```bash
python flask_app.py
```

The Flask app will be available at `http://localhost:5000`

**Using Docker:**
```bash
# Build the Docker image
docker build -t olympic-efficiency:latest .

# Run the container
docker run -p 5000:5000 olympic-efficiency:latest
```

## API Endpoints

### Health Check
```
GET /health
```
Returns the status of the API.

### Predictions
```
POST /predict
Content-Type: application/json

{
  "population": 50000000,
  "gdp_per_capita": 5000,
  "athletes_sent": 300,
  "sports_participated": 25,
  "events_participated": 100
}
```
Returns predicted medal performance.

### Batch Predictions
```
POST /predict_batch
Content-Type: application/json

{
  "data": [
    {
      "population": 50000000,
      "gdp_per_capita": 5000,
      "athletes_sent": 300
    },
    ...
  ]
}
```

## Model Development Details

### Model Comparison
- **Linear Regression**: Baseline model, good interpretability
- **Random Forest**: Captures non-linear relationships, handles missing data well
- **XGBoost**: Strong performance, fast training, handles feature interactions
- **Neural Networks**: For complex pattern recognition

### Hyperparameter Tuning
All models are tuned using grid search with cross-validation. Best parameters are documented in the notebooks and configuration files.

### Key Performance Metrics
- **RMSE**: Root Mean Squared Error for regression accuracy
- **MAE**: Mean Absolute Error for average prediction error
- **R² Score**: Proportion of variance explained by the model

## MLOps Practices

### Version Control
- Git for source code version control
- DVC (Data Version Control) for dataset tracking
- Model versioning with timestamps and performance metrics

### Automated Testing
- Unit tests in the `tests/` folder
- Continuous integration with GitHub Actions
- Pre-commit hooks for code quality checks

### Model Monitoring
- Performance tracking in production
- Data drift detection
- Retraining triggers when performance degrades

### Deployment Pipeline
- Automated testing on commits
- Docker containerization
- Kubernetes deployment (optional)
- Model registry for version management

## Configuration

Key configurations can be found in:
- `config/model_config.yaml`: Model hyperparameters
- `config/data_config.yaml`: Data processing parameters
- `src/utils/constants.py`: Project constants and settings

## Testing

Run unit tests with pytest:
```bash
pytest tests/ -v
```

Run specific test module:
```bash
pytest tests/test_data.py -v
```

Generate coverage report:
```bash
pytest --cov=src tests/
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Performance Results

### Best Performing Models (based on validation set)
- **Regression (Total Medals)**: XGBoost with R² = 0.92
- **Regression (Medals per Athlete)**: Random Forest with R² = 0.88
- **Classification (Medal Performance Category)**: XGBoost with Accuracy = 0.85

See `notebooks/04_model_development.ipynb` for detailed results.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Authors

- Muhammad Farooq (@Muhammad-Farooq-13)

## Contact

For questions or feedback, please reach out to: mfarooqshafee333@gmail.com

## Acknowledgments

- Olympic Dataset Source
- Contributors and maintainers
- Open-source libraries: scikit-learn, pandas, Flask, etc.

## References

- [Scikit-learn Documentation](https://scikit-learn.org/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Docker Documentation](https://docs.docker.com/)
- [MLOps Best Practices](https://ml-ops.systems/)
