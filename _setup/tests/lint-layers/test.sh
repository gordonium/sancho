#!/usr/bin/env bash
# name: test-lint-layers
# type: script
# description: Runs the lint against a fixture tree of deliberately bad files and asserts each one is caught and the good file passes.
# why: The lint is a hook; a hook nobody tests is a hook that silently stopped working.
# reads: _setup/tests/lint-layers/fixture/
# writes: stdout; exit code
# test: (this is the test)
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/../.." && pwd)"
FIX=$(mktemp -d) && [ -d "$FIX" ] || { echo "test-lint-layers: FAIL: no temp dir"; exit 1; }; cp -R "$HERE/fixture/." "$FIX/"; find "$FIX" -name INDEX.md -delete; rm -f "$FIX/_setup/index-manifest.json"
# ERRORS.md #11 (2026-10-02): session notes written now, so "40 minutes ago" is true whenever the test runs. Three notes with a
# stale `next:`: one with a live lease (caught), one whose line became `doing:` (passes), one with no lease (passes).
mkdir -p "$FIX/_queue/sessions" "$FIX/_queue/leases" "$FIX/_design" "$FIX/skills/revived" "$FIX/skills/kept" "$FIX/_setup/templates"
AGO=$(python3 -c "import datetime; print((datetime.datetime.now()-datetime.timedelta(minutes=40)).strftime('%H:%M'))")
SOON=$(python3 -c "import datetime; print((datetime.datetime.now()-datetime.timedelta(minutes=10)).strftime('%H:%M'))")
printf -- '---\nname: s\ntype: doc\nlobe: both\ndescription: session note\n---\n- next: the food routine (announced %s)\n' "$AGO" > "$FIX/_queue/sessions/stale-session.md"
printf -- '---\nname: s\ntype: doc\nlobe: both\ndescription: session note\n---\n- doing: the weekly review (announced %s)\n- next: the map rebuild (announced %s)\n' "$AGO" "$SOON" > "$FIX/_queue/sessions/doing-session.md"
printf -- '---\nname: s\ntype: doc\nlobe: both\ndescription: session note\n---\n- next: the closed thing (announced %s)\n' "$AGO" > "$FIX/_queue/sessions/closed-session.md"
for s in stale-session doing-session; do printf -- '---\nname: %s\ntype: lease\nlobe: both\ndescription: lease\nkind: cowork\n---\n' "$s" > "$FIX/_queue/leases/$s.md"; done
# ERRORS.md #10: a decisions row marked dropped with a lint: field; the phrase in a skill and in a template is caught, a clean skill passes
printf -- '| date | decision | who |\n|---|---|---|\n| 2026-09-29 | **Sensitive set-aside dropped:** facts like any other. lint: [sensitive attribute, "Anything Sensitive"] | Gordon |\n| 2026-09-30 | **Plain row** lint: [plainphrase] | Gordon |\n' > "$FIX/_design/decisions.md"
printf -- '---\nname: revived\n---\nA Sensitive Attribute waits in Open threads.\n' > "$FIX/skills/revived/SKILL.md"
printf -- '---\nname: kept\n---\nFacts like any other; plainphrase is fine.\n' > "$FIX/skills/kept/SKILL.md"
printf -- '---\nname: t\n---\nblocked reason: anything sensitive\n' > "$FIX/_setup/templates/revived-template.md"
out=$(SANCHO_ROOT="$FIX" python3 "$ROOT/lint-layers.py" 2>&1 || true)
fail=0
refuse(){ if echo "$out" | grep -q -- "$1"; then echo "FAIL wrongly flagged: $1"; fail=1; else echo "ok   passed: $1"; fi; }
expect(){ if echo "$out" | grep -q -- "$1"; then echo "ok   caught: $1"; else echo "MISS not caught: $1"; fail=1; fi; }
expect "CLAUDE.md is 1"            # too long
expect "type: person outside people/"
expect "instruction to Claude"
expect "naked.md: no frontmatter"
expect "skill header missing"
expect "external guidance file"
expect "FOCUS.md today work: 4 items"
expect "idea without next_review"
expect "sync conflict copy"
expect "without a same-line"       # unguarded mktemp in a test (ERRORS.md #6)
expect "inferred.md:7: \`timezone\` cites \[gordon\] without his words"
expect "inferred.md:8: inference words"
expect "stale-session.md:7: announced the food routine at $AGO, not started"
refuse "doing-session.md"          # `doing:` is not flagged, and a 10-minute-old next: is not stale
refuse "closed-session.md"         # no live lease
expect "skills/revived/SKILL.md:4: reversed-decision phrase \"sensitive attribute\""
expect "_setup/templates/revived-template.md:4: reversed-decision phrase \"anything sensitive\""
refuse "skills/kept/SKILL.md:4: reversed-decision"
expect "decisions.md:4: a \`lint: \[..\]\` field on a row that does not say"
if echo "$out" | grep -q "good.md"; then echo "FAIL good file flagged"; fail=1; else echo "ok   good file passed"; fi
if echo "$out" | grep -q "stated.md"; then echo "FAIL stated.md flagged"; fail=1; else echo "ok   stated file passed"; fi
rm -rf "$FIX"
[ $fail -eq 0 ] && echo "test-lint-layers: PASS" || { echo "test-lint-layers: FAIL"; exit 1; }
