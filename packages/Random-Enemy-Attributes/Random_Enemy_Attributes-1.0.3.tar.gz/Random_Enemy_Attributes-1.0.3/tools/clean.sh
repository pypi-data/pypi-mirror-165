#!/usr/bin/env bash
SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
rm -rf $SCRIPT_DIR/venv
rm -rf $SCRIPT_DIR/../build
rm -rf $SCRIPT_DIR/../dist
rm -rf $SCRIPT_DIR/../wheelhouse
rm -f $SCRIPT_DIR/../src/Simple_PARAMETER_EDITOR.cpp
rm -f $SCRIPT_DIR/../*.so
rm -rf $SCRIPT_DIR/../*.egg-info
