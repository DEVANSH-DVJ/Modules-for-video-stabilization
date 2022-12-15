# Dataset for Video Stabilization

Summer Undergraduate Research Project (SURP) 2021: Modules for video stabilization

## Setup

```bash
# Setup python3.8 virtual environment
python3.8 -m venv surp
source surp/bin/activate
pip install wheel pathlib
pip install -r requirements.txt

# Unzip dataset
unzip -u data.zip
```

## Usage

```bash
# Verify that the environment is setup correctly
python src/datagen.py data/Map_v1/config.yaml -preview

# Verify that all models are working correctly
./test.sh

# Generate the dataset
./generate.sh
```
