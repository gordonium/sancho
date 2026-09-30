#!/usr/bin/env bash
# name: install-mac
# type: script
# description: Install or reinstall every launchd job in _setup/com.sancho.*.plist: render __HOME__, copy to ~/Library/LaunchAgents, bootout the old one, bootstrap the new. Idempotent. Also makes the executable bits right.
# why: One command rebuilds the Mac side after a change or on a replacement Mac (architecture §6.5 recovery runbook).
# reads: _setup/com.sancho.*.plist
# writes: ~/Library/LaunchAgents/com.sancho.*.plist; launchd state
# test: _setup/tests/install-mac/
set -euo pipefail
SETUP="$(cd "$(dirname "$0")" && pwd)"
LA="${SANCHO_LAUNCH_AGENTS:-$HOME/Library/LaunchAgents}"
LAUNCHCTL="${SANCHO_LAUNCHCTL:-launchctl}"
DOMAIN="gui/$(id -u)"
mkdir -p "$LA" "$HOME/.local/state/sancho"
chmod +x "$SETUP"/*.sh "$SETUP"/hooks/* 2>/dev/null || true
for src in "$SETUP"/com.sancho.*.plist; do
  label=$(basename "$src" .plist); dst="$LA/$label.plist"
  sed "s#__HOME__#$HOME#g" "$src" > "$dst.tmp"
  plutil -lint -s "$dst.tmp" >/dev/null || { echo "bad plist: $src"; rm -f "$dst.tmp"; exit 1; }
  mv "$dst.tmp" "$dst"
  $LAUNCHCTL bootout "$DOMAIN/$label" 2>/dev/null || true
  $LAUNCHCTL bootstrap "$DOMAIN" "$dst"
  echo "loaded $label"
done
