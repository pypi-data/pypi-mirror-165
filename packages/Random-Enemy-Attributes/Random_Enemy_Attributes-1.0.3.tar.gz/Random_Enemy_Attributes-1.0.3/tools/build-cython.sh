#!/usr/bin/env bash
SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PYTHON=$SCRIPT_DIR/venv/bin/python3

cd $SCRIPT_DIR/..

$PYTHON setup.py build_ext --inplace
