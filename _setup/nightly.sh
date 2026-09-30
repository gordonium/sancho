#!/usr/bin/env bash
# name: nightly
# type: command
# description: Regenerate every index, lint, then rebuild the map, in that order; stops at the first failure so a broken lint never produces a map.
# why: Generated files must never drift from the tree (architecture §4, §14); the lint gates the map by design.
# reads: the tree
# writes: every INDEX.md, PROJECTS.md, ICE.md; _setup/LINT.md; MAP.md
# schedule: nightly 02:00 (com.sancho.nightly enqueues it)
# test: _setup/tests/nightly/
set -euo pipefail
cd "${SANCHO_ROOT:-$HOME/Sync/Sancho}"
python3 _setup/build-index.py | tail -1
python3 _setup/lint-layers.py | tail -1
python3 _setup/build-map.py | tail -1
echo "nightly: index, lint, map all ok"
