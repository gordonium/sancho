"""
name: test-pipeline-rematch
type: script
description: earballs.py `rematch`, `retry` and the chunk fallback in a temp tree with a fake voiceprint library and no network. rematch --person --since examines every ready recording in the window where the person was a candidate, newest first, with no cap (26 changed clusters come back, past the old 20), lists only clusters whose top candidate changed (rec_id, handle, old, new, score), leaves out recordings before --since and ones where the person was never a candidate, writes the list to _queue/log/ as it goes and never touches speakers.md. retry puts a recording that failed five times back to `downloaded` with error count 0. A chunk ffmpeg cannot cut by copying is cut by re-encoding.
why: A bad reference can have influenced any recording since its enrollment; truncating the list hides wrong attributions (decisions.md 2026-10-01, "Re-match has no cap"). rec_1716cb70ff failed five times on the copy-cut and was then left for good.
reads: _setup/pipeline/earballs.py, _setup/sancho_lib.py
writes: temp files only
requires: mac
test: (this is the test)
"""
import os, shutil, subprocess, sys, tempfile
from pathlib import Path

SETUP = Path(__file__).resolve().parents[2]
VENV_PY = Path(os.environ.get("SANCHO_VENV", Path.home() / ".local/share/sancho/venv")) / "bin/python"
if not VENV_PY.exists():
    print("test-pipeline-rematch: FAIL: pipeline venv missing (run _setup/pipeline/install-venv.sh)"); sys.exit(1)
T = Path(tempfile.mkdtemp())
if not T.is_dir():
    print("test-pipeline-rematch: FAIL: no temp dir"); sys.exit(1)
tree = T / "tree"; (tree / "_setup/pipeline").mkdir(parents=True); (tree / "people").mkdir(); (tree / "recordings/inbox").mkdir(parents=True)
(tree / "CLAUDE.md").write_text("x")
for f in ("sancho_lib.py", "notify.py", "notify-reasons.md"):
    shutil.copy(SETUP / f, tree / "_setup" / f)
shutil.copy(SETUP / "pipeline/earballs.py", tree / "_setup/pipeline/earballs.py")
bin_dir = T / "bin"; bin_dir.mkdir()
(bin_dir / "ffmpeg").write_text("#!/bin/sh\nfor a in \"$@\"; do last=\"$a\"; [ \"$a\" = copy ] && exit 234; done\necho cut > \"$last\"\n")
(bin_dir / "ffmpeg").chmod(0o755)
ENV = {**os.environ, "SANCHO_ROOT": str(tree), "SANCHO_AUDIO": str(T / "audio"), "SANCHO_STATE": str(T / "state"),
       "SANCHO_SECRETS_PLAIN": str(T / "env"), "PATH": f"{bin_dir}:{os.environ.get('PATH', '')}"}
code = f"""
import sys, io, json, contextlib, numpy as np; sys.argv=['x']
sys.path.insert(0, {str(tree / '_setup/pipeline')!r}); import earballs as e
for d in (e.VOICE_REC, e.VOICE_SPK, e.PROCESSED): d.mkdir(parents=True, exist_ok=True)
ROY, GORDON = [1.0, 0, 0, 0], [0, 1.0, 0, 0]
np.save(e.VOICE_SPK / 'roy.npy', np.array([ROY])); np.save(e.VOICE_SPK / 'gordon.npy', np.array([GORDON]))
(e.VOICE_SPK / '_library.json').write_text(json.dumps({{'speakers': {{'roy': {{'refs': 5, 'recordings': 3}}, 'gordon': {{'refs': 5, 'recordings': 3}}}}}}))
c = e.db()
def rec(rid, ready, cand, vec, status='ready', errors=0):
    loc = f'recordings/inbox/{{rid}}'
    c.execute("INSERT INTO recordings (id, era, status, location, ready_at, error_count, audio_path, last_error) VALUES (?,?,?,?,?,?,?,?)",
              (rid, 'fresh', status, loc if status == 'ready' else None, ready, errors, f'processed/{{rid}}.ogg', 'transcribe: CalledProcessError' if errors else None))
    if status != 'ready': return
    (e.ROOT / loc).mkdir(parents=True, exist_ok=True)
    (e.ROOT / loc / 'speakers.md').write_text(f'---\\nrec_id: {{rid}}\\n---\\n| cluster | talk time | candidate (machine) | confirmed | by | when | note |\\n|---|---|---|---|---|---|---|\\n| SPEAKER_00 | 00:01:00 | {{cand}} sim=0.91 refs=5 |  |  |  |  |\\n')
    if vec is not None:
        np.save(e.VOICE_REC / f'{{rid}}.npy', np.array([vec])); (e.VOICE_REC / f'{{rid}}.labels.json').write_text(json.dumps({{'labels': ['SPEAKER_00']}}))
for i in range(26):   # gordon was the candidate, the voice is roy's: 26 changes, past the old cap of 20
    rec(f'rec_c{{i:09d}}', f'2026-09-{{i + 2:02d}}T10:00:00+00:00', 'gordon', ROY)
rec('rec_same000000', '2026-09-29T10:00:00+00:00', 'gordon', GORDON)      # still gordon: not listed
rec('rec_early00000', '2026-08-01T10:00:00+00:00', 'gordon', ROY)         # before --since
rec('rec_other00000', '2026-09-28T10:00:00+00:00', 'roy', GORDON)         # gordon never a candidate
rec('rec_noemb00000', '2026-09-27T10:00:00+00:00', 'gordon', None)        # no embeddings saved: counted, not guessed
before = (e.ROOT / 'recordings/inbox/rec_c000000000/speakers.md').read_text()
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    rc = e.main(['rematch', '--person', 'gordon', '--since', '2026-09-01'])
out = buf.getvalue(); lines = [l for l in out.splitlines() if l.startswith('rec_')]
assert rc == 0, out
assert len(lines) == 26, f'expected 26 changed, got {{len(lines)}}: {{out}}'
assert lines[0] == 'rec_c000000025\\tSPEAKER_00\\tgordon\\troy\\t1.00', lines[0]      # newest first; rec_id, handle, old, new, score
assert not any(x in out for x in ('rec_same', 'rec_early', 'rec_other')), out
assert '28 had gordon as a candidate, 26 cluster(s) changed, 1 without saved embeddings' in out.splitlines()[-1], out.splitlines()[-1]
logs = list((e.ROOT / '_queue/log').glob('rematch-gordon-*.tsv'))
assert len(logs) == 1 and len(logs[0].read_text().splitlines()) == 27, 'partial-results file missing or short'
assert (e.ROOT / 'recordings/inbox/rec_c000000000/speakers.md').read_text() == before, 'rematch wrote speakers.md'
with contextlib.redirect_stdout(buf):
    assert e.main(['rematch', '--person', 'Gordon; x', '--since', 'yesterday']) == 1

# retry: failed five times -> downloaded, error count 0, audited
rec('rec_failed0000', None, '', None, status='failed', errors=5)
(e.PROCESSED / 'rec_failed0000.ogg').write_bytes(b'OggS' + b'0' * 100)
with contextlib.redirect_stdout(buf):
    assert e.main(['retry', 'rec_failed0000']) == 0
row = c.execute("SELECT status, error_count, next_try_at FROM recordings WHERE id='rec_failed0000'").fetchone()
assert (row['status'], row['error_count'], row['next_try_at']) == ('downloaded', 0, None), dict(row)
assert c.execute("SELECT COUNT(*) FROM audit WHERE rec_id='rec_failed0000' AND stage='retry'").fetchone()[0] == 1
with contextlib.redirect_stdout(buf):
    assert e.main(['retry', 'rec_nope']) == 1

# chunk fallback: the fake ffmpeg exits 234 on `-c copy` and succeeds otherwise
import tempfile, pathlib
work = pathlib.Path(tempfile.mkdtemp(dir={str(T)!r})); big = work / 'big.ogg'; big.write_bytes(b'0' * 4000)
e.GROQ_MAX_BYTES = 1000; e.ffprobe_duration = lambda p: 2400.0
chunks = e.chunk_audio(big, work)
assert len(chunks) >= 2 and all(p.name.endswith('.re.ogg') and p.exists() for _, p in chunks), chunks
print('rematch-ok')
"""
r = subprocess.run([str(VENV_PY), "-c", code], env=ENV, capture_output=True, text=True, timeout=120)
shutil.rmtree(T, ignore_errors=True)
if "rematch-ok" not in r.stdout:
    print("test-pipeline-rematch: FAIL: " + (r.stderr or r.stdout)[-1500:]); sys.exit(1)
print("test-pipeline-rematch: PASS")
