#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if ! command -v uv >/dev/null 2>&1 && ! command -v python3 >/dev/null 2>&1; then
  echo "ci-local.sh: need uv or python3 on PATH" >&2
  exit 1
fi

run_python() {
  if command -v uv >/dev/null 2>&1; then
    uv run --no-project "$@"
  else
    python3 "$@"
  fi
}

if command -v uv >/dev/null 2>&1; then
  uv run --no-project --with pytest==8.4.2 python -m pytest tests/test_policy.py -q
else
  python3 -m pytest tests/test_policy.py -q
fi

run_python -m compileall -q src
