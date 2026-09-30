#!/usr/bin/env bash
# name: ping
# type: command
# description: Round-trip test for the queue. Echoes the request id it was given.
# why: Startup's daily self-test needs one command that cannot fail for any reason but the bridge itself.
# reads: nothing
# writes: stdout (the watcher wraps it into a result file)
# test: _setup/tests/ping/
echo "pong ${1:-${SANCHO_REQUEST_ID:-no-id}} $(date -u +%FT%TZ)"
