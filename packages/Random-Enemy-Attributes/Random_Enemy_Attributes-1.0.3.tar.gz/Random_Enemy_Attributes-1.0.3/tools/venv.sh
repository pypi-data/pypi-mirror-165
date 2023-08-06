#!/usr/bin/env bash
SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PYTHON=$SCRIPT_DIR/venv/bin/python3

echo "Creating Virtual Enviornment..."
python3 -m venv $SCRIPT_DIR/venv
echo "Instaling build requirements..."
$PYTHON -m pip install --upgrade wheel auditwheel pip twine
echo "Installing cython requirements..."
$PYTHON -m pip install -r $SCRIPT_DIR/../requirements.txt
