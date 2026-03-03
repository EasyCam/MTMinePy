#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "=== MTMinePy PyPI Upload Script ==="

# Check required tools
for cmd in python3 pip; do
    if ! command -v "$cmd" &>/dev/null; then
        echo "Error: $cmd is not installed."
        exit 1
    fi
done

# Install build dependencies if missing
python3 -m pip install --upgrade build twine

# Clean previous builds
echo "Cleaning old build artifacts..."
rm -rf dist/ build/ *.egg-info

# Build the package
echo "Building package..."
python3 -m build

# Show built files
echo ""
echo "Built packages:"
ls -lh dist/

# Choose upload target
echo ""
read -rp "Upload to [1] PyPI (default) or [2] TestPyPI? " choice

case "$choice" in
    2)
        echo "Uploading to TestPyPI..."
        python3 -m twine upload --repository testpypi dist/*
        echo ""
        echo "Done! View at: https://test.pypi.org/project/mtminepy/"
        ;;
    *)
        echo "Uploading to PyPI..."
        python3 -m twine upload dist/*
        echo ""
        echo "Done! View at: https://pypi.org/project/mtminepy/"
        ;;
esac
