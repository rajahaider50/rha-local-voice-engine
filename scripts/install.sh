#!/bin/bash
echo "Installing RHA Local Voice Engine (Linux standard setup)..."

# Create venv
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install -U pip
pip install -r requirements.txt

echo "Setup Complete."
