#!/bin/bash
set -e
set -o pipefail

echo ""
echo "[ 1/4 ] isort — sorting imports..."
uv run isort src

echo ""
echo "[ 2/4 ] ruff format — formatting code..."
uv run ruff format src

echo ""
echo "[ 3/4 ] ruff check — checking lint rules..."
uv run ruff check src --fix

echo ""
echo "[ 4/4 ] mypy — checking types..."
uv run mypy src

echo ""
echo "====== all checks completed ======"
