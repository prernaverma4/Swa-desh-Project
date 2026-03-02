#!/bin/bash

# Digital Catalyst - Quick Start Installation Script
# This script automates the setup process

echo "=================================="
echo "Digital Catalyst - Quick Setup"
echo "=================================="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv
echo "✓ Virtual environment created"
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
echo "✓ Dependencies installed"
echo ""

# Initialize database
echo "Initializing database..."
echo "The application will auto-create the database on first run."
echo ""

# Display success message
echo "=================================="
echo "✓ Setup Complete!"
echo "=================================="
echo ""
echo "To start the application:"
echo "1. Activate virtual environment: source venv/bin/activate"
echo "2. Run the app: python app.py"
echo "3. Open browser: http://localhost:5000"
echo ""
echo "Default login credentials:"
echo "Username: admin"
echo "Password: admin123"
echo ""
echo "Happy coding! 🚀"
