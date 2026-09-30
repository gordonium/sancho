#!/usr/bin/env bash
# name: nerd-run-probe
# type: script
# description: Run INSIDE a live Nerd session to prove its confinement: each line prints ALLOWED or BLOCKED for one attempt. Expected: web blocked, write outside the tree blocked, secrets unreadable, write inside the tree allowed.
# why: the sandbox's behaviour is only known by trying it from inside.
# reads: attempts ~/.ssh/config, ~/.config/sancho/env, https://example.com
# writes: attempts ~/nerd-probe.txt (should fail) and _queue/results/nerd-probe-inside.txt (should succeed)
# test: used by the live check recorded in _design/decisions.md 2026-09-30
r(){ if eval "$2" >/dev/null 2>&1; then echo "$1: ALLOWED"; else echo "$1: BLOCKED"; fi; }
r "web (python https example.com)" "python3 -c 'import urllib.request; urllib.request.urlopen(\"https://example.com\", timeout=10)'"
r "write outside tree (~/nerd-probe.txt)" "echo x > \$HOME/nerd-probe.txt"
r "read ~/.ssh/config" "cat \$HOME/.ssh/config"
r "read secrets env" "cat \$HOME/.config/sancho/env"
r "write inside tree" "echo ok > _queue/results/nerd-probe-inside.txt"
rm -f "$HOME/nerd-probe.txt" _queue/results/nerd-probe-inside.txt 2>/dev/null
