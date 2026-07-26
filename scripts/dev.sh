#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if [[ ! -f .venv/bin/python ]]; then
  echo "No existe .venv. Ejecutá: python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt && playwright install chromium" >&2
  exit 1
fi

exec .venv/bin/python run.py "$@"
