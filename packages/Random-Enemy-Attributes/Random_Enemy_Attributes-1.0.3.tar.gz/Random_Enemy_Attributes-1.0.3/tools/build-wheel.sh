#!/usr/bin/env bash
SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PYTHON=$SCRIPT_DIR/venv/bin/python3

cd $SCRIPT_DIR/..

rm -rf dist

echo "Building files..."
$PYTHON setup.py build_ext --inplace
echo "Building wheel..."
$PYTHON setup.py sdist bdist_wheel
echo "Patching wheel..."
$PYTHON -m auditwheel repair $SCRIPT_DIR/../dist/*linux_x86_64.whl
mv $SCRIPT_DIR/../wheelhouse/*.whl $SCRIPT_DIR/../dist
rm -f $SCRIPT_DIR/../dist/*linux_x86_64.whl
rm -rf wheelhouse
