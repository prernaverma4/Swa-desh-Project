#!/usr/bin/env bash
# Digital Catalyst - Run script (installs deps if needed, then starts app)

set -e
cd "$(dirname "$0")"

# Use venv if present
if [ -d ".venv" ]; then
    PYTHON=".venv/bin/python"
    PIP=".venv/bin/pip"
else
    PYTHON="python3"
    PIP="pip3"
fi

# Check if Flask is installed
if ! $PYTHON -c "import flask" 2>/dev/null; then
    echo "Installing dependencies..."
    $PIP install -r requirements.txt 2>/dev/null || \
    $PIP install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
fi

echo "Starting Digital Catalyst on http://127.0.0.1:5001"
$PYTHON app.py
