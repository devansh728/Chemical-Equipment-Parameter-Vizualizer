#!/bin/bash

echo "==============================================="
echo "Chemical Equipment Visualizer - Desktop App"
echo "==============================================="
echo ""

# Activate virtual environment
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
else
    echo "ERROR: Virtual environment not found!"
    echo "Please run ./install.sh first"
    exit 1
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "WARNING: .env file not found!"
    echo "Creating from template..."
    cp .env.example .env
    echo ""
    echo "Please edit .env to configure your backend URL"
    read -p "Press Enter to continue or Ctrl+C to exit and configure first"
fi

echo "Starting Chemical Equipment Visualizer..."
echo ""
echo "Make sure your Django backend is running at:"
grep API_BASE_URL .env
echo ""

python main.py
