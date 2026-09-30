#!/usr/bin/env bash
# name: stay-awake
# type: command
# description: `on` keeps the Mac from idle-sleeping (caffeinate -i -s under launchd, survives the session); `off` stops it; `status` prints the state. State is recorded for HEALTH.md.
# why: Long runs (backfill, big transcriptions) die when the Mac sleeps (architecture §16.3). Note: closing the lid still sleeps a laptop unless it is on power with a display attached.
# reads: launchctl state
# writes: ~/Library/LaunchAgents/com.sancho.caffeinate.plist; ~/.local/state/sancho/stay-awake
# test: _setup/tests/stay-awake/
set -euo pipefail
LA="${SANCHO_LAUNCH_AGENTS:-$HOME/Library/LaunchAgents}"
STATE="${SANCHO_STATE:-$HOME/.local/state/sancho}"
LAUNCHCTL="${SANCHO_LAUNCHCTL:-launchctl}"
PL="$LA/com.sancho.caffeinate.plist"; DOMAIN="gui/$(id -u)"
mkdir -p "$STATE" "$LA"
case "${1:-status}" in
  on)
    cat > "$PL" <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
  <key>Label</key><string>com.sancho.caffeinate</string>
  <key>ProgramArguments</key><array><string>/usr/bin/caffeinate</string><string>-i</string><string>-s</string></array>
  <key>KeepAlive</key><true/>
  <key>RunAtLoad</key><true/>
</dict></plist>
PLIST
    $LAUNCHCTL bootout "$DOMAIN/com.sancho.caffeinate" 2>/dev/null || true
    $LAUNCHCTL bootstrap "$DOMAIN" "$PL"
    echo "on since $(date '+%Y-%m-%d %H:%M')" > "$STATE/stay-awake"
    echo "stay-awake: on (lid-closed sleep still happens unless on power with a display)";;
  off)
    $LAUNCHCTL bootout "$DOMAIN/com.sancho.caffeinate" 2>/dev/null || true
    rm -f "$PL"
    echo "off" > "$STATE/stay-awake"
    echo "stay-awake: off";;
  status)
    echo "stay-awake: $(cat "$STATE/stay-awake" 2>/dev/null || echo off)";;
  *) echo "usage: stay-awake.sh on|off|status"; exit 64;;
esac
