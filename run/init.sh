#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

python3 -m venv "$SCRIPT_DIR/.venv"
source "$SCRIPT_DIR/.venv/bin/activate"
pip install Pillow
