#!/bin/bash

# Stop script on error
set -e

echo "Setting up the Patent application..."

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "Python3 not found. Please install Python3."
    exit 1
fi

# Upgrade pip
echo "🔄 Upgrading pip..."
pip3 install --upgrade pip

# Install dependencies from requirements.txt
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

# Create a virtual environment
if [ ! -d "venv" ]; then
    echo "Creating a virtual environment..."
    python3 -m venv venv
fi

# Activate the virtual environment
echo "Activating virtual environment..."
source venv/bin/activate


# Run the FastAPI server
echo "🚀 Running FastAPI server..."
uvicorn backend.main:app --reload