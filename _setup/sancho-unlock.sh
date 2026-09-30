#!/usr/bin/env bash
# name: sancho-unlock
# type: command
# description: Decrypt ~/Sync/Sancho-Secrets/sancho.env.age to ~/.config/sancho/env (mode 600). Asks for Gordon's passphrase, so it runs in Terminal, never through the queue.
# why: Credentials live in Sync only encrypted (architecture §6.5); a new Mac is working again after one passphrase.
# reads: ~/Sync/Sancho-Secrets/sancho.env.age ($SANCHO_SECRETS_AGE); $SANCHO_AGE_IDENTITY (key file instead of passphrase; tests)
# writes: ~/.config/sancho/env ($SANCHO_SECRETS_PLAIN), mtime set equal to the .age file so the lint sees it as in step
# test: _setup/tests/secrets/
set -euo pipefail
AGE_FILE="${SANCHO_SECRETS_AGE:-$HOME/Sync/Sancho-Secrets/sancho.env.age}"
PLAIN="${SANCHO_SECRETS_PLAIN:-$HOME/.config/sancho/env}"
command -v age >/dev/null || { echo "age not installed (brew install age)"; exit 1; }
[ -f "$AGE_FILE" ] || { echo "no encrypted secrets at $AGE_FILE"; exit 1; }
mkdir -p "$(dirname "$PLAIN")"; chmod 700 "$(dirname "$PLAIN")"
umask 077
tmp="$PLAIN.tmp.$$"
if [ -n "${SANCHO_AGE_IDENTITY:-}" ]; then age -d -i "$SANCHO_AGE_IDENTITY" -o "$tmp" "$AGE_FILE"; else age -d -o "$tmp" "$AGE_FILE"; fi
chmod 600 "$tmp"; touch -r "$AGE_FILE" "$tmp"; mv "$tmp" "$PLAIN"
echo "unlocked: $PLAIN ($(grep -c '=' "$PLAIN") entries)"
