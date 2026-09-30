#!/usr/bin/env bash
# name: earballs-run
# type: command
# description: Run earballs.py under the pipeline venv with the given subcommand (sync, backfill, reprocess, library, status).
# why: The pipeline needs the venv's Python (requests, numpy, pyannote); the watcher and launchd call this one wrapper.
# reads: ~/.local/share/sancho/venv
# writes: whatever earballs.py writes
# test: _setup/tests/pipeline/
VENV="${SANCHO_VENV:-$HOME/.local/share/sancho/venv}"
[ -x "$VENV/bin/python" ] || { echo "pipeline venv missing: run _setup/pipeline/install-venv.sh"; exit 1; }
export PATH="/opt/homebrew/bin:$PATH"
exec "$VENV/bin/python" "$(dirname "$0")/earballs.py" "${@:-sync}"
