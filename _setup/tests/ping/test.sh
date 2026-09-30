#!/usr/bin/env bash
# name: test-ping
# type: script
# description: ping.sh echoes the id it is given.
# why: the queue's round-trip test must itself be tested.
# reads: nothing
# writes: stdout
# test: (this is the test)
out=$(bash "$(dirname "$0")/../../ping.sh" abc123); echo "$out" | grep -q "pong abc123" && echo "test-ping: PASS" || { echo "test-ping: FAIL: $out"; exit 1; }
