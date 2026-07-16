#!/usr/bin/env bash
set -euo pipefail

if command -v glpsol &>/dev/null; then
    echo "glpsol already installed: $(which glpsol)"
    exit 0
fi

echo "glpsol not found. Installing via Homebrew..."
if ! command -v brew &>/dev/null; then
    echo "Error: Homebrew not installed. Install from https://brew.sh"
    exit 1
fi

brew install glpk
echo "GLPK installed: $(which glpsol)"
