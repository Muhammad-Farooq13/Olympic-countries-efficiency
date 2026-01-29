#!/usr/bin/env python3
"""
Project verification script - Ensures all files are properly configured for GitHub upload.
Run this before uploading to GitHub.

Usage:
    python verify_project.py
"""

import os
import sys
from pathlib import Path

def verify_project():
    """Verify project structure and configuration."""
    
    errors = []
    warnings = []
    passed = []
    
    print("=" * 70)
    print("🔍 OLYMPIC COUNTRIES EFFICIENCY PROJECT VERIFICATION")
    print("=" * 70)
    print()
    
    # Check essential directories
    print("📁 Checking Directory Structure...")
    required_dirs = [
        'data/raw', 'data/processed',
        'notebooks',
        'src', 'src/data', 'src/features', 'src/models', 'src/visualization', 'src/utils',
        'tests',
        'config',
        'models',
        'logs'
    ]
    
    for dir_name in required_dirs:
        if os.path.isdir(dir_name):
            passed.append(f"✓ Directory exists: {dir_name}")
        else:
            errors.append(f"✗ Missing directory: {dir_name}")
    
    print()
    
    # Check essential files
    print("📄 Checking Essential Files...")
    required_files = {
        'README.md': 'documentation',
        'QUICKSTART.md': 'documentation',
        'CONTRIBUTING.md': 'documentation',
        'LICENSE': 'license',
        'requirements.txt': 'dependencies',
        'setup.py': 'setup',
        '.gitignore': 'git config',
        'Dockerfile': 'deployment',
        'docker-compose.yaml': 'deployment',
        'flask_app.py': 'application',
        'mlops_pipeline.py': 'application',
        'src/__init__.py': 'source code',
        'src/data/data_loader.py': 'source code',
        'src/features/feature_engineer.py': 'source code',
        'src/models/train.py': 'source code',
        'src/visualization/plots.py': 'source code',
        'src/utils/helpers.py': 'source code',
        'tests/test_data.py': 'tests',
        'tests/test_models.py': 'tests',
        'notebooks/01_eda.ipynb': 'notebooks',
        'notebooks/02_preprocessing.ipynb': 'notebooks',
        'config/pipeline_config.yaml': 'configuration',
    }
    
    for file_name, file_type in required_files.items():
        if os.path.isfile(file_name):
            passed.append(f"✓ File exists: {file_name} ({file_type})")
        else:
            errors.append(f"✗ Missing file: {file_name} ({file_type})")
    
    print()
    
    # Check configuration
    print("⚙️  Checking Configuration...")
    
    # Check author info in key files
    config_checks = {
        'README.md': ('Muhammad Farooq', 'Author name'),
        'setup.py': ('Muhammad Farooq', 'Author in setup.py'),
        'README.md': ('mfarooqshafee333@gmail.com', 'Email address'),
        'setup.py': ('mfarooqshafee333@gmail.com', 'Email in setup.py'),
        'README.md': ('Muhammad-Farooq-13', 'GitHub username'),
    }
    
    checked_files = set()
    for file_name, (search_text, check_name) in config_checks.items():
        if file_name in checked_files:
            continue
        
        if os.path.isfile(file_name):
            with open(file_name, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                if search_text in content:
                    passed.append(f"✓ {check_name} configured correctly")
                else:
                    warnings.append(f"⚠ {check_name} may not be configured - check {file_name}")
            checked_files.add(file_name)
    
    print()
    
    # Check Git configuration
    print("🔐 Checking Git Configuration...")
    if os.path.isfile('.gitignore'):
        with open('.gitignore', 'r') as f:
            gitignore = f.read()
            if '__pycache__' in gitignore and 'venv' in gitignore:
                passed.append("✓ .gitignore properly configured")
            else:
                warnings.append("⚠ .gitignore may be incomplete")
    else:
        errors.append("✗ .gitignore not found")
    
    print()
    
    # Print results
    print("=" * 70)
    print("VERIFICATION RESULTS")
    print("=" * 70)
    print()
    
    if passed:
        print(f"✅ PASSED ({len(passed)} checks):")
        for msg in passed[:5]:
            print(f"   {msg}")
        if len(passed) > 5:
            print(f"   ... and {len(passed) - 5} more")
        print()
    
    if warnings:
        print(f"⚠️  WARNINGS ({len(warnings)} items):")
        for msg in warnings:
            print(f"   {msg}")
        print()
    
    if errors:
        print(f"❌ ERRORS ({len(errors)} items):")
        for msg in errors:
            print(f"   {msg}")
        print()
    
    # Summary
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    
    total_checks = len(passed) + len(warnings) + len(errors)
    
    if not errors:
        print("✅ PROJECT READY FOR GITHUB UPLOAD!")
        print()
        print("Owner Information:")
        print("  Name: Muhammad Farooq")
        print("  Email: mfarooqshafee333@gmail.com")
        print("  GitHub: Muhammad-Farooq-13")
        print()
        print("To upload to GitHub:")
        print("  1. Initialize git: git init")
        print("  2. Add files: git add .")
        print("  3. Commit: git commit -m 'Initial commit'")
        print("  4. Add remote: git remote add origin https://github.com/Muhammad-Farooq-13/olympic-countries-efficiency.git")
        print("  5. Push: git push -u origin main")
        print()
        return 0
    else:
        print("❌ SOME ISSUES FOUND")
        print()
        print(f"Total checks: {total_checks}")
        print(f"  Passed: {len(passed)}")
        print(f"  Warnings: {len(warnings)}")
        print(f"  Errors: {len(errors)}")
        print()
        print("Please fix errors before uploading to GitHub.")
        print()
        return 1

if __name__ == '__main__':
    sys.exit(verify_project())
