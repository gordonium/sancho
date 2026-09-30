#!/usr/bin/env bash
# name: sancho-lock-secrets
# type: command
# description: Re-encrypt ~/.config/sancho/env to ~/Sync/Sancho-Secrets/sancho.env.age after any edit. Asks for the passphrase twice, so it runs in Terminal, never through the queue. Keeps the previous encrypted copy as sancho.env.age.prev.
# why: The Sync copy must always be current (architecture §6.5); the lint fails the build while the plaintext is newer.
# reads: ~/.config/sancho/env ($SANCHO_SECRETS_PLAIN); $SANCHO_AGE_RECIPIENT (public key instead of passphrase; tests)
# writes: ~/Sync/Sancho-Secrets/sancho.env.age ($SANCHO_SECRETS_AGE) and .prev
# test: _setup/tests/secrets/
set -euo pipefail
AGE_FILE="${SANCHO_SECRETS_AGE:-$HOME/Sync/Sancho-Secrets/sancho.env.age}"
PLAIN="${SANCHO_SECRETS_PLAIN:-$HOME/.config/sancho/env}"
command -v age >/dev/null || { echo "age not installed (brew install age)"; exit 1; }
[ -f "$PLAIN" ] || { echo "no plaintext at $PLAIN; nothing to lock"; exit 1; }
mkdir -p "$(dirname "$AGE_FILE")"
tmp="$AGE_FILE.tmp.$$"
if [ -n "${SANCHO_AGE_RECIPIENT:-}" ]; then age -r "$SANCHO_AGE_RECIPIENT" -o "$tmp" "$PLAIN"; else age -p -o "$tmp" "$PLAIN"; fi
[ -f "$AGE_FILE" ] && cp -p "$AGE_FILE" "$AGE_FILE.prev"
mv "$tmp" "$AGE_FILE"; touch -r "$AGE_FILE" "$PLAIN"
echo "locked: $AGE_FILE"
