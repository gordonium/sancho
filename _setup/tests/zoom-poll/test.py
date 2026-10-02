"""
name: test-zoom-poll
type: script
description: zoom-poll.py against a fake Zoom API (the script's one network door, `_open`, is replaced in-process; no socket, so it also runs inside the Nerd sandbox) and a fixture VTT, in a temp tree: missing credentials exit 0 with "zoom: not configured" and one MAC-SETUP.md line, never a second; a meeting with a VTT lands as transcript.md / speakers.md / meta.md in recordings/inbox/<rec_id>/ plus the VTT and M4A in Sancho-Audio/zoom/<date>_<slug>/, participant labels verbatim, exact name or alias matches as `source: zoom-label` candidates and never confirmed, a ledger row with source zoom; a meeting with no VTT goes to the Groq stages after the grace period and waits before it; metered mode defers the MP4 and queues zoom.video, which fetches it once unmetered; a second poll lands nothing twice; a failing poll turns the watchdog red only after 24 h with a fresh failure; the sync's 15-minute clock enqueues zoom.poll.
why: The poll runs unattended every 15 minutes; a regression means Zoom meetings silently stop arriving (must-never 10) or a typed display name becomes a confirmed identity (must-never 7). Gap: Zoom's real API has not been called; the response shapes are from Zoom's documentation, not a capture.
reads: _setup/zoom-poll.py, _setup/pipeline/earballs.py, _setup/sancho_lib.py, _setup/tests/zoom-poll/fixture.vtt
writes: temp files only
test: (this is the test)
"""
import datetime as dt, importlib.util, io, json, os, re, shutil, sqlite3, subprocess, sys, tempfile, urllib.error
from pathlib import Path
from urllib.parse import urlparse, parse_qs, unquote

HERE = Path(__file__).resolve().parent
SETUP = HERE.parents[1]
T = Path(tempfile.mkdtemp())
if not T.is_dir():
    print("test-zoom-poll: FAIL: no temp dir"); sys.exit(1)
def fail(m):
    print(f"test-zoom-poll: FAIL: {m}"); shutil.rmtree(T, ignore_errors=True); sys.exit(1)
def check(cond, m):
    if not cond: fail(m)

def make_tree(name, env_text):
    tree = T / name
    (tree / "_setup").mkdir(parents=True); (tree / "people").mkdir(); (tree / "recordings/inbox").mkdir(parents=True)
    (tree / "CLAUDE.md").write_text("x")
    (tree / "_setup/MAC-SETUP.md").write_text("---\nname: setup\ntype: doc\ndescription: fixture\n---\n# setup\n")
    (tree / "env").write_text(env_text)
    return tree, {"SANCHO_ROOT": str(tree), "SANCHO_AUDIO": str(T / name / "audio"), "SANCHO_STATE": str(T / name / "state"), "SANCHO_SECRETS_PLAIN": str(tree / "env")}

clean = {k: v for k, v in os.environ.items() if not k.startswith(("ZOOM", "SANCHO_"))}

# --- 1. missing credentials: exit clean, ask once
tree1, e1 = make_tree("none", "GROQ_API_KEY=g\n")
for i in (1, 2):
    r = subprocess.run([sys.executable, str(SETUP / "zoom-poll.py")], env={**clean, **e1}, capture_output=True, text=True, timeout=60)
    check(r.returncode == 0, f"unconfigured run {i} exit {r.returncode}: {r.stderr[-800:]}")
    check("zoom: not configured" in r.stdout, f"unconfigured run {i} said: {r.stdout!r}")
setup = (tree1 / "_setup/MAC-SETUP.md").read_text()
check(setup.count("Zoom is not configured") == 1 and "recording:read:admin" in setup and "ZOOM_CLIENT_SECRET" in setup, "MAC-SETUP.md should carry exactly one Zoom line naming the scope and the keys")
check(len([ln for ln in setup.splitlines() if "Zoom" in ln]) == 1, "the Zoom ask must be one line")
check("Zoom: not configured" in (tree1 / "recordings/STATUS.md").read_text(), "STATUS.md should say Zoom is not configured")
check(not list((tree1 / "recordings/inbox").iterdir()) and not (tree1 / "_queue").exists(), "an unconfigured poll must land and queue nothing")

# --- 2. configured, fake API, in-process
tree, e2 = make_tree("live", "ZOOM_ACCOUNT_ID=acct\nZOOM_CLIENT_ID=cid\nZOOM_CLIENT_SECRET=sec\nGROQ_API_KEY=g\n")
(tree / "people/gordon.md").write_text("---\nname: Gordon Seirup\naliases: [Gordon]\ntype: person\nlobe: both\ndescription: fixture\n---\n")
(tree / "people/pat-example.md").write_text("---\nname: Pat Example\naliases: [Pat, iPhone (Pat)]\ntype: person\nlobe: both\ndescription: fixture\n---\n")
for k in list(os.environ):
    if k.startswith("ZOOM"): del os.environ[k]
os.environ.update(e2)
spec = importlib.util.spec_from_file_location("zoom_poll", SETUP / "zoom-poll.py")
zp = importlib.util.module_from_spec(spec); spec.loader.exec_module(zp)
eb = zp.eb
check(str(eb.ROOT) == str(tree.resolve()) or str(eb.ROOT) == str(tree), f"the test must run in its temp tree, not {eb.ROOT}")

now = dt.datetime.now(dt.timezone.utc).replace(microsecond=0)
iso = lambda t: t.isoformat().replace("+00:00", "Z")
def meeting(uuid, topic, start, mins, kinds):
    files = [{"id": f"{uuid}-{k}", "file_type": k, "recording_type": {"TRANSCRIPT": "audio_transcript", "M4A": "audio_only", "MP4": "shared_screen_with_speaker_view"}[k],
              "status": "completed", "file_size": 2048, "download_url": f"https://files.zoom.fake/dl/{uuid}-{k}",
              "recording_start": iso(start), "recording_end": iso(start + dt.timedelta(minutes=mins))} for k in kinds]
    return {"uuid": uuid, "id": 8123456789, "topic": topic, "start_time": iso(start), "duration": mins, "timezone": "Europe/Rome", "host_email": "host@example.invalid", "recording_files": files}
S1 = now - dt.timedelta(hours=26)
MEETINGS = [meeting("m1uuid==", "Weekly Sync: Acme / Q3 | plan", S1, 30, ["MP4", "M4A", "TRANSCRIPT"]),
            meeting("/m2/uuid", "No transcript call", now - dt.timedelta(hours=6), 30, ["M4A"]),
            meeting("m3uuid", "Just ended", now - dt.timedelta(minutes=50), 30, ["M4A"])]
MEDIA = b"\x00\x00\x00\x20ftypM4A " + b"\x00" * 2036
BODY = {"TRANSCRIPT": (HERE / "fixture.vtt").read_bytes(), "M4A": MEDIA, "MP4": MEDIA}
F = {"calls": [], "token_fail": False}
def fake_open(url, headers=None, data=None, method="GET", timeout=120):
    u = urlparse(url); F["calls"].append((method, url, dict(headers or {})))
    if u.path == "/oauth/token":
        if F["token_fail"]:
            raise urllib.error.HTTPError(url, 401, "Unauthorized", {}, io.BytesIO(b'{"reason":"Invalid client_id or client_secret"}'))
        check(method == "POST" and headers["Authorization"].startswith("Basic ") and "account_id=acct" in u.query, "token request shape")
        return io.BytesIO(json.dumps({"access_token": "tok"}).encode())
    check((headers or {}).get("Authorization") == "Bearer tok", f"no bearer token on {url}")
    if u.path == "/v2/users/me/recordings":
        q = parse_qs(u.query)
        return io.BytesIO(json.dumps({"meetings": [m for m in MEETINGS if q["from"][0] <= m["start_time"][:10] <= q["to"][0]]}).encode())
    if u.path.startswith("/v2/meetings/"):
        uuid = unquote(unquote(u.path.split("/")[3]))
        return io.BytesIO(json.dumps(next(m for m in MEETINGS if m["uuid"] == uuid)).encode())
    if u.path.startswith("/dl/"):
        return io.BytesIO(BODY[u.path.rsplit("-", 1)[1]])
    fail(f"unexpected request {method} {url}")
zp._open = fake_open
zp.online = lambda: True
state = Path(e2["SANCHO_STATE"]); state.mkdir(parents=True)
def network(metered):
    (state / "network.json").write_text(json.dumps({"metered": metered, "label": "phone-hotspot" if metered else "home"}))
def ledger():
    c = sqlite3.connect(Path(e2["SANCHO_AUDIO"]) / "ledger.sqlite", isolation_level=None); c.row_factory = sqlite3.Row; return c
def run(fn):
    out, old = io.StringIO(), sys.stdout
    sys.stdout = out
    try: code = fn()
    finally: sys.stdout = old
    return code, out.getvalue()

# --- poll on a metered network
network(True)
code, out = run(zp.cmd_poll)
check(code == 0, f"poll exit {code}: {out}")
from zoneinfo import ZoneInfo
day = S1.astimezone(ZoneInfo("Europe/Rome")).date().isoformat()
folder = Path(e2["SANCHO_AUDIO"]) / "zoom" / f"{day}_weekly-sync-acme-q3-plan"
check(folder.is_dir(), f"storage folder missing; have {[p.name for p in (Path(e2['SANCHO_AUDIO']) / 'zoom').iterdir()]}")
check(sorted(p.name for p in folder.iterdir()) == ["audio_only.m4a", "audio_transcript.vtt"], f"metered: VTT and M4A only, got {sorted(p.name for p in folder.iterdir())}")
check((folder / "audio_transcript.vtt").read_bytes() == BODY["TRANSCRIPT"], "the VTT is stored as Zoom sent it")
inbox = sorted(p for p in (tree / "recordings/inbox").iterdir())
check(len(inbox) == 1 and re.fullmatch(r"rec_[0-9a-f]{10}", inbox[0].name), f"one rec_ folder expected in the inbox, got {[p.name for p in inbox]}")
rid = inbox[0].name
check(sorted(p.name for p in inbox[0].iterdir()) == ["meta.md", "speakers.md", "transcript.md"], f"landing files: {sorted(p.name for p in inbox[0].iterdir())}")
tr, sp, mt = [(inbox[0] / n).read_text() for n in ("transcript.md", "speakers.md", "meta.md")]
for label, stamp in (("Gordon Seirup", "00:00:02"), ("Dana Q. Fixture-Person", "00:00:07"), ("iPhone (Pat)", "00:00:25"), ("(no label)", "00:00:22")):
    check(f"**{label}** [{stamp}]" in tr, f"transcript lacks **{label}** [{stamp}]")
check("Yes: loud and clear. I have the numbers for the quarter." in tr, "consecutive cues of one speaker should join, text after the label kept whole")
check("Note: this line has no participant label." in tr and "**Note**" not in tr, "a one-off 'Note:' in a file with unlabelled cues is text, not a participant")
check("source: zoom" in tr and "backend: zoom vtt" in tr and f"rec_id: {rid}" in tr, "transcript frontmatter")
rows = {c[0]: c for c in ([x.strip() for x in ln.strip().strip("|").split("|")] for ln in sp.splitlines() if ln.startswith("| ") and not ln.startswith("| cluster"))}
check(set(rows) == {"Gordon Seirup", "Dana Q. Fixture-Person", "iPhone (Pat)", "(no label)"}, f"speakers.md rows: {sorted(rows)}")
check(rows["Gordon Seirup"][2] == "gordon source: zoom-label", f"exact name match should be a zoom-label candidate: {rows['Gordon Seirup']}")
check(rows["iPhone (Pat)"][2] == "pat-example source: zoom-label", f"exact alias match should be a zoom-label candidate: {rows['iPhone (Pat)']}")
check(rows["Dana Q. Fixture-Person"][2] == "Dana Q. Fixture-Person" and rows["Dana Q. Fixture-Person"][6] == "Zoom participant label; confirm the person slug", f"unmatched label row: {rows['Dana Q. Fixture-Person']}")
check(all(r[3] == "" and r[4] == "" and r[5] == "" for r in rows.values()), "no Zoom row may be confirmed by the machine (must-never 7)")
check(rows["Gordon Seirup"][1] == "00:00:18", f"talk time: {rows['Gordon Seirup'][1]}")
for want in ("| source | zoom |", "Weekly Sync: Acme / Q3 / plan", "| host | host@example.invalid |", "Gordon Seirup, Dana Q. Fixture-Person, iPhone (Pat)", "| duration | 00:30:00 |",
             f"Sancho-Audio/zoom/{folder.name}/audio_transcript.vtt (done)", f"Sancho-Audio/zoom/{folder.name}/audio_only.m4a (done)",
             f"Sancho-Audio/zoom/{folder.name}/shared_screen_with_speaker_view.mp4 (deferred", "Groq not used"):
    check(want in mt, f"meta.md lacks: {want}")
c = ledger()
row = c.execute("SELECT * FROM recordings WHERE id=?", (rid,)).fetchone()
check(row and row["source"] == "zoom" and row["status"] == "ready" and row["location"] == f"recordings/inbox/{rid}" and row["backend"] == "zoom"
      and row["audio_path"] == f"zoom/{folder.name}/audio_only.m4a" and row["era"] == "fresh" and row["sha256"], f"ledger row: {dict(row) if row else None}")
g = c.execute("SELECT * FROM recordings WHERE source='zoom' AND id!=?", (rid,)).fetchall()
check(len(g) == 1 and g[0]["status"] == "downloaded" and g[0]["title"] == "No transcript call" and g[0]["location"] is None and g[0]["audio_path"].endswith("audio_only.m4a"),
      "a meeting with no VTT past the grace period is one ledger row at 'downloaded' for the Groq stages")
check(c.execute("SELECT state FROM zoom_meetings WHERE uuid='m3uuid'").fetchone()[0] == "waiting", "a meeting that just ended waits for Zoom's transcript")
check(c.execute("SELECT state FROM zoom_files WHERE file_type='MP4'").fetchone()[0] == "deferred", "metered: MP4 deferred")
check(eb.meta_get(c, "zoom_last_poll_ok"), "the last poll is state in the ledger")
vreq = list((tree / "_queue/requests").glob("*_zoom.video_*.md"))
check(len(vreq) == 1 and "args: [video]" in vreq[0].read_text(), "one zoom.video request queued for the deferred MP4")
st = (tree / "recordings/STATUS.md").read_text()
check("Zoom: 2 meeting(s) landed (1 from Zoom's transcript, 1 via Groq), 1 waiting" in st and "1 waiting for zoom.video" in st, f"STATUS.md Zoom line: {[l for l in st.splitlines() if 'Zoom' in l]}")
check(not any("groq" in u.lower() for _, u, _ in F["calls"]), "Groq must not be called for a meeting with a VTT")

# --- a second poll lands nothing twice; zoom.video while metered fetches nothing
code, out = run(zp.cmd_poll)
check(code == 0 and len(list((tree / "recordings/inbox").iterdir())) == 1 and c.execute("SELECT COUNT(*) FROM recordings").fetchone()[0] == 2, f"second poll must not land again: {out}")
check(len(list((tree / "_queue/requests").glob("*_zoom.video_*.md"))) == 1, "no second zoom.video while one waits")
code, out = run(zp.cmd_video)
check(code == 0 and "deferred" in out and not list(folder.glob("*.mp4")), f"zoom.video on a metered network must fetch nothing: {out}")

# --- unmetered: the video arrives
network(False)
code, out = run(zp.cmd_video)
check(code == 0 and (folder / "shared_screen_with_speaker_view.mp4").read_bytes() == MEDIA, f"unmetered zoom.video should fetch the MP4: {out}")
check(c.execute("SELECT state FROM zoom_files WHERE file_type='MP4'").fetchone()[0] == "done", "MP4 state done")
check(sorted(p.name for p in inbox[0].iterdir()) == ["meta.md", "speakers.md", "transcript.md"] and (inbox[0] / "meta.md").read_text() == mt, "the landed files are not rewritten when the video arrives")

# --- a failing poll: exit 1, shown at once, red only after 24 h with a fresh failure; recovery clears it
F["token_fail"] = True
code, out = run(zp.cmd_poll)
check(code == 1 and "poll failed" in out, f"a refused token is a failed poll: {code} {out}")
check("poll failing since" in (tree / "recordings/STATUS.md").read_text(), "STATUS.md should show the failing poll")
check(not [p for p in eb.problems(c) if p[1] == "zoom"], "a poll failing for minutes is not yet a watchdog problem")
eb.meta_set(c, "zoom_fail_since", iso(now - dt.timedelta(hours=25)))
check([p[0] for p in eb.problems(c) if p[1] == "zoom"] == ["critical"], "red for 24 h with a fresh failure → critical (the pipeline red alert rule)")
eb.meta_set(c, "zoom_last_fail", iso(now - dt.timedelta(hours=3)))
check(not [p for p in eb.problems(c) if p[1] == "zoom"], "a day asleep is not a day of failing")
F["token_fail"] = False
code, out = run(zp.cmd_poll)
check(code == 0 and eb.meta_get(c, "zoom_fail_since") is None, "a good poll clears the failure")

# --- the 15-minute clock in the pipeline sync
check(eb.zoom_schedule(c) is True and len(list((tree / "_queue/requests").glob("*_zoom.poll_*.md"))) == 1, "configured: the sync enqueues zoom.poll")
req = next((tree / "_queue/requests").glob("*_zoom.poll_*.md"))
check("requested_by: launchd" in req.read_text(), "the scheduled request is marked launchd (it waits for the Mac to settle)")
check(eb.zoom_schedule(c) is False, "not while one waits")
req.unlink()
check(eb.zoom_schedule(c) is False, "not again within 15 minutes")
eb.meta_set(c, "zoom_enqueued_at", iso(now - dt.timedelta(minutes=16)))
check(eb.zoom_schedule(c) is True, "again after 15 minutes")
c1 = sqlite3.connect(Path(e1["SANCHO_AUDIO"]) / "ledger.sqlite")
check(c1.execute("SELECT COUNT(*) FROM recordings").fetchone()[0] == 0, "the unconfigured run left no ledger rows")

shutil.rmtree(T, ignore_errors=True)
print("test-zoom-poll: PASS")
