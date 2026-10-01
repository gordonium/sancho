#!/usr/bin/env bash
# name: test-quarantine-guard-runner
# type: script
# description: Runs the real suite, test.py, beside this file (test-all picks test.sh first; this replaced Cowork's failing placeholder on 2026-10-01). Whether the hook is registered on this Mac is not tested here: HEALTH.md reports it every tick.
# why: ERRORS.md #9. One suite, one entry point.
# reads: test.py
# writes: nothing (test.py uses temp files only)
# test: (this is the test)
exec python3 "$(cd "$(dirname "$0")" && pwd)/test.py"
