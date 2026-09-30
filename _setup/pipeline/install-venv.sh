#!/usr/bin/env bash
# name: install-venv
# type: script
# description: Create or update the pipeline's Python 3.12 venv at ~/.local/share/sancho/venv from _setup/pipeline/requirements.txt.
# why: The pipeline needs requests, numpy and pyannote; a venv inside Sync corrupts, so it lives outside and is rebuilt from the pinned list (recovery runbook step).
# reads: _setup/pipeline/requirements.txt
# writes: ~/.local/share/sancho/venv
# test: _setup/tests/pipeline/ (checks the venv imports when present)
set -euo pipefail
VENV="${SANCHO_VENV:-$HOME/.local/share/sancho/venv}"
PY=/opt/homebrew/bin/python3.12
[ -x "$PY" ] || { echo "python3.12 missing (brew install python@3.12)"; exit 1; }
[ -x "$VENV/bin/python" ] || "$PY" -m venv "$VENV"
"$VENV/bin/pip" install -q --upgrade pip
"$VENV/bin/pip" install -q -r "$(dirname "$0")/requirements.txt"
echo "venv ready: $VENV ($("$VENV/bin/python" --version))"
