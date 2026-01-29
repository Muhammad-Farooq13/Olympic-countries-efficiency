# 📑 PROJECT INDEX & NAVIGATION GUIDE

## 🎯 Where to Start?

### 👤 I'm a Data Scientist
1. Start with: [QUICKSTART.md](QUICKSTART.md)
2. Explore: [notebooks/01_eda.ipynb](notebooks/01_eda.ipynb)
3. Learn: [src/data/data_loader.py](src/data/data_loader.py)
4. Practice: [notebooks/02_preprocessing.ipynb](notebooks/02_preprocessing.ipynb)

### 👨‍💻 I'm a Software Engineer
1. Start with: [README.md](README.md#deployment)
2. Setup: [flask_app.py](flask_app.py)
3. Deploy: [Dockerfile](Dockerfile)
4. Test: [tests/test_models.py](tests/test_models.py)

### 🚀 I'm DevOps/Platform Engineer
1. Start with: [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md#docker-operations)
2. Review: [docker-compose.yaml](docker-compose.yaml)
3. Setup: [.github/workflows/ci_cd.yaml](.github/workflows/ci_cd.yaml)
4. Monitor: [mlops_pipeline.py](mlops_pipeline.py)

### 📊 I'm a Project Manager
1. Start with: [PROJECT_COMPLETION.md](PROJECT_COMPLETION.md)
2. Understand: [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md)
3. Review: [CONTRIBUTING.md](CONTRIBUTING.md)
4. Plan: [README.md](README.md#installation-and-setup)

---

## 📚 Documentation Map

### Quick References
| Document | Purpose | Time |
|----------|---------|------|
| [QUICKSTART.md](QUICKSTART.md) | Get running in 5 minutes | 5 min |
| [README.md](README.md) | Full documentation | 15 min |
| [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md) | Structure & features | 10 min |

### Detailed Guides
| Document | Purpose | Time |
|----------|---------|------|
| [CONTRIBUTING.md](CONTRIBUTING.md) | How to contribute | 5 min |
| [LICENSE](LICENSE) | MIT License terms | 2 min |
| [PROJECT_COMPLETION.md](PROJECT_COMPLETION.md) | What's included | 10 min |

---

## 🔍 Finding Code

### By Functionality
| Need | File |
|------|------|
| Load data | [src/data/data_loader.py](src/data/data_loader.py) |
| Clean data | [src/data/data_loader.py](src/data/data_loader.py) |
| Engineer features | [src/features/feature_engineer.py](src/features/feature_engineer.py) |
| Train models | [src/models/train.py](src/models/train.py) |
| Plot data | [src/visualization/plots.py](src/visualization/plots.py) |
| Make predictions | [predict_example.py](predict_example.py) |
| Serve API | [flask_app.py](flask_app.py) |
| Run pipeline | [mlops_pipeline.py](mlops_pipeline.py) |

### By Layer
| Layer | Location |
|-------|----------|
| Data | [src/data/](src/data/) |
| Features | [src/features/](src/features/) |
| Models | [src/models/](src/models/) |
| Visualization | [src/visualization/](src/visualization/) |
| Utils | [src/utils/](src/utils/) |
| Tests | [tests/](tests/) |

---

## 📖 Reading Order for Learning

### Beginner Path
1. [QUICKSTART.md](QUICKSTART.md) - Get setup
2. [notebooks/01_eda.ipynb](notebooks/01_eda.ipynb) - Explore data
3. [README.md](README.md#methodology) - Learn methodology
4. [notebooks/02_preprocessing.ipynb](notebooks/02_preprocessing.ipynb) - Clean data

### Intermediate Path
1. [src/features/feature_engineer.py](src/features/feature_engineer.py) - Feature engineering
2. [src/models/train.py](src/models/train.py) - Model training
3. [mlops_pipeline.py](mlops_pipeline.py) - Pipeline automation
4. [tests/](tests/) - Testing patterns

### Advanced Path
1. [flask_app.py](flask_app.py) - API design
2. [Dockerfile](Dockerfile) - Containerization
3. [.github/workflows/ci_cd.yaml](.github/workflows/ci_cd.yaml) - CI/CD
4. [config/pipeline_config.yaml](config/pipeline_config.yaml) - Configuration

---

## 🎓 Common Tasks

### Task: Setup Environment
**Time**: 5 minutes
```bash
pip install -r requirements.txt
pip install -e .
```
→ See: [QUICKSTART.md](QUICKSTART.md#installation)

### Task: Explore Dataset
**Time**: 15 minutes
```bash
jupyter notebook notebooks/01_eda.ipynb
```
→ See: [notebooks/01_eda.ipynb](notebooks/01_eda.ipynb)

### Task: Train Model
**Time**: 10 minutes
```bash
python mlops_pipeline.py --config config/pipeline_config.yaml
```
→ See: [mlops_pipeline.py](mlops_pipeline.py)

### Task: Start API Server
**Time**: 2 minutes
```bash
python flask_app.py
```
→ See: [flask_app.py](flask_app.py), [README.md](README.md#api-endpoints)

### Task: Run Tests
**Time**: 5 minutes
```bash
pytest tests/ -v
```
→ See: [tests/](tests/)

### Task: Deploy with Docker
**Time**: 5 minutes
```bash
docker-compose up
```
→ See: [docker-compose.yaml](docker-compose.yaml), [README.md](README.md#docker-deployment)

### Task: Make Predictions
**Time**: 5 minutes
```bash
python predict_example.py --input data.csv
```
→ See: [predict_example.py](predict_example.py)

---

## 🔧 Configuration

### Model Settings
**File**: [config/pipeline_config.yaml](config/pipeline_config.yaml)
**Contains**:
- Data paths
- Model hyperparameters
- Training settings
- Logging configuration

### Python Dependencies
**File**: [requirements.txt](requirements.txt)
**Contains**:
- ML libraries (pandas, scikit-learn, xgboost)
- Web framework (Flask)
- Testing (pytest)
- Deployment (Docker)

### Flask Configuration
**File**: [flask_app.py](flask_app.py)
**Environment Variables**:
- `MODEL_PATH` - Path to model file
- `SCALER_PATH` - Path to scaler
- `FEATURE_NAMES_PATH` - Path to features

### Docker Configuration
**File**: [Dockerfile](Dockerfile)
**File**: [docker-compose.yaml](docker-compose.yaml)
**Ports**: 5000 (Flask API)

---

## 📊 Data

### Dataset Location
- **Raw**: [data/raw/olympic_countries_efficiency.csv](../data/raw/olympic_countries_efficiency.csv)
- **Processed**: [data/processed/](data/processed/) (created by pipeline)

### Dataset Size
- **Rows**: 250+
- **Columns**: 18
- **Time Period**: 1992-2016

### Target Variables
- `total_medals` - Regression target
- `medals_per_athlete` - Efficiency metric

---

## 🧪 Testing

### Test Files
- [tests/test_data.py](tests/test_data.py) - Data loading tests
- [tests/test_models.py](tests/test_models.py) - Model tests

### Run Tests
```bash
# All tests
pytest tests/ -v

# With coverage
pytest --cov=src tests/

# Specific test
pytest tests/test_data.py -v
```

---

## 📈 Metrics & Monitoring

### Saved Artifacts
- **Model**: [models/best_model.pkl](models/best_model.pkl)
- **Scaler**: [models/scaler.pkl](models/scaler.pkl)
- **Features**: [models/feature_names.pkl](models/feature_names.pkl)

### Generated Reports
- **Plots**: [outputs/plots/](outputs/plots/)
- **Metrics**: [outputs/metrics/](outputs/metrics/)
- **Reports**: [outputs/reports/](outputs/reports/)

### Logs
- **Pipeline**: [logs/mlops_pipeline.log](logs/mlops_pipeline.log)
- **API**: [logs/app.log](logs/app.log) (generated at runtime)

---

## 🚀 Deployment Options

### Option 1: Local Python
```bash
python flask_app.py
```
→ See: [README.md](README.md#local-setup)

### Option 2: Docker Container
```bash
docker build -t olympic-efficiency .
docker run -p 5000:5000 olympic-efficiency
```
→ See: [Dockerfile](Dockerfile)

### Option 3: Docker Compose
```bash
docker-compose up
```
→ See: [docker-compose.yaml](docker-compose.yaml)

### Option 4: Cloud Deployment
→ See: [README.md](README.md#deployment)

---

## 🤝 Contributing

**Contribution Guide**: [CONTRIBUTING.md](CONTRIBUTING.md)

### Steps:
1. Fork repository
2. Create feature branch
3. Make changes
4. Run tests: `pytest tests/`
5. Submit pull request

### Code Standards
- PEP 8 formatting
- Docstring every function
- Test coverage > 80%
- Passing CI/CD

---

## 🐛 Troubleshooting

### Issue: Module not found
**Solution**: `pip install -e .`

### Issue: Port 5000 in use
**Solution**: `python flask_app.py --port 5001`

### Issue: Model not loading
**Solution**: Check `models/best_model.pkl` exists

### Issue: Docker build fails
**Solution**: `docker build --no-cache -t olympic-efficiency .`

### For More Help
→ See: [README.md](README.md#troubleshooting)

---

## 📞 Getting Help

1. **Quick Answer**: [QUICKSTART.md](QUICKSTART.md)
2. **Full Documentation**: [README.md](README.md)
3. **Project Details**: [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md)
4. **Contributing**: [CONTRIBUTING.md](CONTRIBUTING.md)
5. **Issues**: Open GitHub issue
6. **Email**: See README.md for contact

---

## 🗂️ File Organization

### Root Level
- Setup & run: [setup.sh](setup.sh), [setup.bat](setup.bat)
- API: [flask_app.py](flask_app.py)
- Pipeline: [mlops_pipeline.py](mlops_pipeline.py)
- Prediction: [predict_example.py](predict_example.py)
- Data: [olympic_countries_efficiency.csv](olympic_countries_efficiency.csv)

### Configuration
- Pipeline: [config/pipeline_config.yaml](config/pipeline_config.yaml)
- Dependencies: [requirements.txt](requirements.txt), [setup.py](setup.py)
- Docker: [Dockerfile](Dockerfile), [docker-compose.yaml](docker-compose.yaml)
- Git: [.gitignore](.gitignore)
- CI/CD: [.github/workflows/ci_cd.yaml](.github/workflows/ci_cd.yaml)

### Documentation
- Overview: [README.md](README.md)
- Quick Start: [QUICKSTART.md](QUICKSTART.md)
- Structure: [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md)
- Completion: [PROJECT_COMPLETION.md](PROJECT_COMPLETION.md)
- Contributing: [CONTRIBUTING.md](CONTRIBUTING.md)
- License: [LICENSE](LICENSE)

### Code
- Data: [src/data/](src/data/)
- Features: [src/features/](src/features/)
- Models: [src/models/](src/models/)
- Visualization: [src/visualization/](src/visualization/)
- Utilities: [src/utils/](src/utils/)

### Other
- Notebooks: [notebooks/](notebooks/)
- Tests: [tests/](tests/)
- Data: [data/](data/)
- Models: [models/](models/)
- Outputs: [outputs/](outputs/)
- Logs: [logs/](logs/)

---

## ✅ Quick Checklist

- [ ] Read [QUICKSTART.md](QUICKSTART.md)
- [ ] Run `pip install -r requirements.txt`
- [ ] Explore [notebooks/01_eda.ipynb](notebooks/01_eda.ipynb)
- [ ] Run `python mlops_pipeline.py`
- [ ] Start `python flask_app.py`
- [ ] Test API: `curl http://localhost:5000/health`
- [ ] Run tests: `pytest tests/ -v`
- [ ] Read [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 📞 Support Path

```
Question/Issue
    ↓
Check [README.md](README.md) FAQ
    ↓
Search [QUICKSTART.md](QUICKSTART.md)
    ↓
Review [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md)
    ↓
Check [CONTRIBUTING.md](CONTRIBUTING.md)
    ↓
Open GitHub Issue
```

---

**Last Updated**: January 29, 2024
**Project Version**: 0.1.0
**Status**: ✅ Ready to Use

Happy coding! 🚀
