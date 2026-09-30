#!/usr/bin/env python3
"""
name: test-sancho_lib
type: script
description: Unit checks for the frontmatter reader: inline maps with # inside quotes, block lists, python docstring headers.
why: Every generator trusts this reader.
reads: nothing
writes: stdout
test: (this is the test)
"""
import sys, tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from sancho_lib import read_frontmatter
d = Path(tempfile.mkdtemp())
f = d / "a.md"
f.write_text('---\nname: X\nnext_action: {text: "build order #6; go", set: 2026-09-30}\ntags: [a, b]\nroles:\n  - {context: w, role: r}\n  - {context: p, role: f}\n---\nbody\n')
fm, body = read_frontmatter(f)
assert fm["name"] == "X", fm
assert fm["next_action"]["text"] == "build order #6; go", fm["next_action"]
assert fm["tags"] == ["a", "b"], fm
assert len(fm["roles"]) == 2 and fm["roles"][1]["role"] == "f", fm["roles"]
assert body.strip() == "body"
py = d / "s.py"; py.write_text('#!/usr/bin/env python3\n"""\nname: s\ntype: command\ndescription: d\n"""\nprint(1)\n')
fm, _ = read_frontmatter(py); assert fm["type"] == "command", fm
print("test-sancho_lib: PASS")
