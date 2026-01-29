# Quick Start Guide

## Installation

### 1. Clone and Setup
```bash
cd olympic-countries-efficiency
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install -e .
```

### 2. Run the Pipeline
```bash
python mlops_pipeline.py --config config/pipeline_config.yaml --mode train
```

### 3. Start Flask Application
```bash
# Local
python flask_app.py

# Docker
docker build -t olympic-efficiency:latest .
docker run -p 5000:5000 olympic-efficiency:latest
```

## Project Structure
```
olympic-countries-efficiency/
├── data/                    # Data folder
│   ├── raw/                 # Original dataset
│   └── processed/           # Cleaned data
├── notebooks/               # Jupyter notebooks
├── src/                     # Source code
│   ├── data/               # Data loading
│   ├── features/           # Feature engineering
│   ├── models/             # Model training
│   ├── visualization/      # Plots
│   └── utils/              # Helper functions
├── tests/                  # Unit tests
├── models/                 # Saved models
├── config/                 # Configuration files
├── flask_app.py            # Flask server
├── mlops_pipeline.py       # ML pipeline
├── requirements.txt        # Dependencies
└── README.md              # Full documentation
```

## Key Files

| File | Purpose |
|------|---------|
| `mlops_pipeline.py` | Complete ML workflow automation |
| `flask_app.py` | Model serving API |
| `src/data/data_loader.py` | Data loading & cleaning |
| `src/features/feature_engineer.py` | Feature engineering |
| `src/models/train.py` | Model training & evaluation |
| `Dockerfile` | Docker containerization |

## API Endpoints

- `GET /health` - Health check
- `GET /info` - API information
- `GET /model_details` - Model metadata
- `POST /predict` - Single prediction
- `POST /predict_batch` - Batch predictions

Example request:
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "population": 50000000,
    "gdp_per_capita": 5000,
    "athletes_sent": 300
  }'
```

## Testing

```bash
pytest tests/ -v
pytest --cov=src tests/
```

## Troubleshooting

**Model not loading?**
- Check model file exists: `models/best_model.pkl`
- Verify scaler file: `models/scaler.pkl`

**Flask port 5000 in use?**
```bash
python flask_app.py --port 5001
```

**Python version issues?**
- Ensure Python 3.8+: `python --version`
- Use `python3` if `python` doesn't work

## Next Steps

1. Review [README.md](README.md) for detailed documentation
2. Explore [notebooks/](notebooks/) for analysis examples
3. Check [CONTRIBUTING.md](CONTRIBUTING.md) to contribute
4. See [LICENSE](LICENSE) for usage terms

## Support

For issues or questions, please open an issue on GitHub or contact the maintainers.

---
**Happy analyzing!** 🚀
