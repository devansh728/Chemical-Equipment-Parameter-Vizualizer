#!/bin/bash

echo "==============================================="
echo "Chemical Equipment Visualizer - Desktop App"
echo "==============================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo ""
fi

echo "Activating virtual environment..."
source venv/bin/activate
echo ""

echo "Installing dependencies..."
pip install -r requirements.txt
echo ""

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo ""
    echo "IMPORTANT: Please edit .env file to configure your backend URL"
    echo ""
fi

echo "==============================================="
echo "Installation complete!"
echo "==============================================="
echo ""
echo "To run the application:"
echo "  1. Make sure Django backend is running"
echo "  2. Run: ./run.sh"
echo ""
