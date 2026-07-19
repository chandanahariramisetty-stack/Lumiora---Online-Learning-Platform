#!/bin/bash

echo "=========================================="
echo "   LUMIORA - Online Learning Platform"
echo "=========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "[ERROR] Python is not installed"
        echo "Please install Python from https://python.org"
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

echo "[1/4] Python found: $($PYTHON_CMD --version)"
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "[2/4] Creating virtual environment..."
    $PYTHON_CMD -m venv venv
else
    echo "[2/4] Virtual environment already exists"
fi

# Activate virtual environment
echo "[3/4] Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "[4/4] Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "=========================================="
echo "   Starting Lumiora Server..."
echo "=========================================="
echo ""
echo "Open your browser and go to: http://127.0.0.1:5000"
echo ""
echo "Press CTRL+C to stop the server"
echo ""

$PYTHON_CMD app.py

echo ""
echo "Server stopped."
