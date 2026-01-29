from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="olympic-countries-efficiency",
    version="0.1.0",
    author="Muhammad Farooq",
    author_email="mfarooqshafee333@gmail.com",
    description="Olympic Countries Efficiency Analysis and Prediction",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Muhammad-Farooq-13/olympic-countries-efficiency",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pandas>=1.5.0",
        "numpy>=1.24.0",
        "scikit-learn>=1.3.0",
        "xgboost>=2.0.0",
        "flask>=2.3.0",
        "matplotlib>=3.7.0",
        "seaborn>=0.12.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.7.0",
            "flake8>=6.0.0",
            "pylint>=2.17.0",
        ],
        "gpu": [
            "tensorflow[and-cuda]>=2.13.0",
        ],
    },
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "olympic-train=src.models.train:main",
            "olympic-predict=src.models.predict:main",
        ],
    },
)
