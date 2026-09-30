#!/usr/bin/env bash
# name: notify-test
# type: command
# description: Send one test push through notify.py at the given level (info|warn|alert; default info). The message carries the time, so dedupe never swallows it.
# why: The phone channel is proven by a real message arriving, on demand.
# reads: PUSHOVER_USER, PUSHOVER_TOKEN (env)
# writes: one Pushover message
# test: _setup/tests/notify/ (notify.py itself; this wrapper is one line)
LEVEL="${1:-info}"
exec python3 "$(dirname "$0")/notify.py" "$LEVEL" "Sancho test push ($LEVEL) $(date '+%Y-%m-%d %H:%M %Z')" --key=notify.test
