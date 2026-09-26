#!/bin/bash
echo "Setting up RHA Local Voice Engine for Termux..."

# 1. Update and install dependencies
pkg update -y
pkg upgrade -y
pkg install -y python clang cmake make git libffi openssl pkg-config
pkg install -y sqlite

# Install Termux API for Android integrations (battery, volume, apps)
pkg install -y termux-api

# Audio deps
pkg install -y pulseaudio libportaudio

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate

# 3. Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

echo "To install AI dependencies, check device RAM and run:"
echo "CMAKE_ARGS=\"-DGGML_TERMUX=ON\" pip install llama-cpp-python"

echo "Termux Setup Complete."
echo "Make sure you install the 'Termux:API' app from F-Droid to allow the engine to control your phone!"
