#!/usr/bin/env bash
SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
mkdir -p build
gcc $SCRIPT_DIR/../PARAMETEREDITOR/Simple_PARAMETER_EDITOR.cpp -o $SCRIPT_DIR/../build/PARAMETEREDITOR
