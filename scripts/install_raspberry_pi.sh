#!/usr/bin/env bash
set -euo pipefail

python_bin="${PYTHON_BIN:-python3}"

sudo apt update
sudo apt install -y python3 python3-venv python3-pip build-essential cmake

"$python_bin" -m venv .venv
source .venv/bin/activate

python -m pip install -U pip setuptools wheel
python -m pip install -e .
python -m pip install -r requirements-pi.txt

echo "Install complete. Run:"
echo "source .venv/bin/activate"
echo "python -m lightweight_llm_pi --demo"
