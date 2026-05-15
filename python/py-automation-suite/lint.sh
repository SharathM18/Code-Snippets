#!/usr/bin/env bash

# ==========================================================================================
# Script Name: lint.sh
# Description: Execute the static code analysis and formatting pipeline.
#              Runs isort (imports), ruff (formatting/linting), mypy (types),
#              and shellcheck (bash validation) to enforce code quality standards.
# Author:      [your name/team]
# Date:        2026-05-15
# Usage:       uv run bash lint.sh
# ==========================================================================================

set -euo pipefail

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
echo "[ 5/5 ] shellcheck - checking bash scripts..."
shellcheck *.sh

echo ""
echo "====== all checks completed ======"
