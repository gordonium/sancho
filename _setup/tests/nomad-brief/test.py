"""
name: test-nomad-brief
type: script
description: nomad-brief.py and the people/_geo.json generator against fake Open-Meteo geocoding, Open-Meteo forecast and NWS alerts (the script's one network door, `_get`, is replaced in-process; no socket, so it also runs inside the Nerd sandbox), in a temp tree with the real thresholds file: in range -> stay; out of range tomorrow with one in-range candidate east at 100 miles -> "drive today: east, 100 miles"; out only on day three -> drive in the next couple of days; a Severe/Extreme alert -> wait; wind over the line flagged, never decided; no in-range direction -> wait; freeze tonight flagged regardless; outside the US -> alerts skipped with a note and NWS never called; a people file within reach appears (pending city geocoded by the brief, cached city placed offline by build-index, non-places skipped); one forecast call carries all 33 points; unknown location -> exit 2, failed forecast -> exit 1, no brief either way.
why: The morning verdict is computed, never guessed (personal-morning step 4); a regression means a wrong driving day or a dropped person. Gap: the live APIs are not called here; response shapes are from Open-Meteo's and NWS's documentation, not a capture.
reads: _setup/nomad-brief.py, _setup/build-index.py, _setup/sancho_lib.py, personal/nomad/thresholds.md
writes: temp files only
test: (this is the test)
"""
import importlib.util, json, os, shutil, subprocess, sys, tempfile, urllib.error
from pathlib import Path
from urllib.parse import urlparse, parse_qs

HERE = Path(__file__).resolve().parent
SETUP = HERE.parents[1]
REAL = SETUP.parent
T = Path(tempfile.mkdtemp())
if not T.is_dir():
    print("test-nomad-brief: FAIL: no temp dir"); sys.exit(1)
def fail(m):
    print(f"test-nomad-brief: FAIL: {m}"); shutil.rmtree(T, ignore_errors=True); sys.exit(1)
def check(cond, m):
    if not cond: fail(m)

sys.path.insert(0, str(SETUP))
from sancho_lib import city_query  # noqa: E402

# --- 0. the city reader on the shapes the people files really carry
check(city_query("Austin, TX area")[1:] == ("Austin", "TX"), f"Austin, TX area -> {city_query('Austin, TX area')}")
check(city_query("Fort Collins CO [inferred: a street number]")[1:] == ("Fort Collins", "CO"), "Fort Collins CO [inferred …]")
check(city_query("in the wind; public land in the Rockies")[0] is None, "'in the wind' is not a place")
check(city_query("Australia (city not stated)")[0] is None, "'city not stated' is not a place")
check(city_query(None) == (None, "blank", ""), "blank city")
check(city_query("Tropea")[1:] == ("Tropea", ""), "bare city")

# --- the temp tree
tree = T / "tree"
for d in ("_setup", "people", "personal/nomad/log"):
    (tree / d).mkdir(parents=True)
(tree / "CLAUDE.md").write_text("x")
shutil.copy(REAL / "personal/nomad/thresholds.md", tree / "personal/nomad/thresholds.md")
(tree / "personal/nomad/location.md").write_text("---\nname: loc\ntype: doc\nlobe: personal\ndescription: fixture\n---\ncity: unknown (not stated)\n")
person = lambda slug, name, city, wtsb="": (tree / f"people/{slug}.md").write_text(
    f"---\nname: {name}\ntype: person\nlobe: both\ndescription: fixture\nlocation: {{city: {city}, as_of: 2026-09-01, source: \"\"}}\nlast_seen: 2026-09-24\nwant_to_see_by: {wtsb}\n---\n")
person("pat-example", "Pat Example", '"Bastrop, TX"', "2026-10-12")
person("wren-example", "Wren Example", '"Windsor, CO"')
person("drifter-example", "Drifter Example", '"in the wind; public land in the Rockies"')
person("blank-example", "Blank Example", "")
(tree / "personal/nomad/_geocache.json").write_text(json.dumps({"windsor|co": {"lat": 40.4775, "lon": -104.9014, "label": "Windsor, Colorado, United States", "country_code": "US"}}))
env = {**{k: v for k, v in os.environ.items() if not k.startswith("SANCHO_")}, "SANCHO_ROOT": str(tree)}
r = subprocess.run([sys.executable, str(SETUP / "build-index.py")], env=env, capture_output=True, text=True, timeout=120)
check(r.returncode == 0, f"build-index crashed: {r.stderr[-800:]}")
geo = json.loads((tree / "people/_geo.json").read_text())
gp = {p["slug"]: p for p in geo["people"]}
check(set(gp) == {"pat-example", "wren-example"}, f"_geo.json people: {sorted(gp)}")
check(gp["pat-example"]["pending"] and gp["pat-example"]["lat"] is None and gp["pat-example"]["want_to_see_by"] == "2026-10-12", f"uncached city should be pending: {gp['pat-example']}")
check(not gp["wren-example"]["pending"] and gp["wren-example"]["lat"] == 40.4775, f"cached city should be placed offline: {gp['wren-example']}")
check([s["slug"] for s in geo["skipped"]] == ["drifter-example"], f"skipped: {geo['skipped']}")
check("people/_geo.json" in json.loads((tree / "_setup/index-manifest.json").read_text())["files"], "_geo.json must be in the generated-file manifest")

# --- the fake network
os.environ["SANCHO_ROOT"] = str(tree)
spec = importlib.util.spec_from_file_location("nomad_brief", SETUP / "nomad-brief.py")
nb = importlib.util.module_from_spec(spec); spec.loader.exec_module(nb)
AUSTIN = (30.2672, -97.7431)
PLACES = {
    "Austin": [{"name": "Austin", "latitude": 43.6666, "longitude": -92.9746, "feature_code": "PPLA2", "country_code": "US", "country": "United States", "admin1": "Minnesota", "timezone": "America/Chicago"},
               {"name": "Austin", "latitude": AUSTIN[0], "longitude": AUSTIN[1], "feature_code": "PPLA", "country_code": "US", "country": "United States", "admin1": "Texas", "timezone": "America/Chicago"}],
    "Bastrop": [{"name": "Bastrop", "latitude": 30.1105, "longitude": -97.3153, "feature_code": "PPLA2", "country_code": "US", "country": "United States", "admin1": "Texas", "timezone": "America/Chicago"}],
    "Tropea": [{"name": "Tropea", "latitude": 38.6767, "longitude": 15.8984, "feature_code": "PPL", "country_code": "IT", "country": "Italy", "admin1": "Calabria", "timezone": "Europe/Rome"}],
}
COOL = {"highs": [80, 80, 80, 80], "lows": [55, 55, 55, 55], "wind": [10, 10, 10, 10]}
HOT = {"highs": [95, 95, 95, 95], "lows": [72, 72, 72, 72], "wind": [10, 10, 10, 10]}
S = {"weather": lambda lat, lon: COOL, "alerts": {}, "forecast_error": False}
calls = []
DATES = ["2026-10-02", "2026-10-03", "2026-10-04", "2026-10-05"]

def point_weather(w, lat, lon):
    hourly_t, hourly_v = [], []
    for i, d in enumerate(DATES):
        for h in range(24):
            hourly_t.append(f"{d}T{h:02d}:00")
            hourly_v.append(w["lows"][i] if h >= 18 else (w["lows"][max(i - 1, 0)] if h < 9 else w["highs"][i]))
    tz = "Europe/Rome" if lon > 0 else "America/Chicago"
    return {"latitude": lat, "longitude": lon, "timezone": tz, "timezone_abbreviation": "CEST" if lon > 0 else "CDT", "utc_offset_seconds": 0,
            "daily": {"time": DATES, "temperature_2m_max": w["highs"], "temperature_2m_min": w["lows"], "wind_speed_10m_max": w["wind"], "precipitation_sum": [0.0, 0.1, 0, 0]},
            "hourly": {"time": hourly_t, "temperature_2m": hourly_v}}

def fake_get(url, headers=None, timeout=30):
    u = urlparse(url); q = parse_qs(u.query)
    calls.append((u.netloc, url, dict(headers or {})))
    if u.netloc == "geocoding-api.open-meteo.com":
        return json.dumps({"results": PLACES.get(q["name"][0], [])}).encode()
    if u.netloc == "api.open-meteo.com":
        if S["forecast_error"]:
            raise urllib.error.URLError("network down")
        check(q["temperature_unit"] == ["fahrenheit"] and q["wind_speed_unit"] == ["mph"] and q["timezone"] == ["auto"], f"forecast units/timezone: {q}")
        lats, lons = [float(x) for x in q["latitude"][0].split(",")], [float(x) for x in q["longitude"][0].split(",")]
        out = [point_weather(S["weather"](a, b), a, b) for a, b in zip(lats, lons)]
        return json.dumps(out if len(out) > 1 else out[0]).encode()
    if u.netloc == "api.weather.gov":
        pt = q["point"][0]
        return json.dumps({"features": [{"properties": a} for a in S["alerts"].get(pt, [])]}).encode()
    fail(f"unexpected URL {url}")
nb._get = fake_get

def run(*args):
    calls.clear()
    for f in (tree / "personal/nomad").glob("brief-*"):
        f.unlink()
    code = nb.main(list(args))
    md, js = tree / "personal/nomad/brief-2026-10-02.md", tree / "personal/nomad/brief-2026-10-02.json"
    return code, (json.loads(js.read_text()) if js.exists() else None), (md.read_text() if md.exists() else "")

def ring_pt(bearing, miles, home=AUSTIN):
    return nb.destination(home[0], home[1], bearing, miles)
EAST_IN = {ring_pt(90, m) for m in (100, 150, 200)}
def east_only(here_w):
    def w(lat, lon):
        if (round(lat, 4), round(lon, 4)) == AUSTIN:
            return here_w
        return COOL if (round(lat, 4), round(lon, 4)) in EAST_IN else HOT
    return w

# --- 1. in range -> stay; people in reach; pending city geocoded and cached
code, b, md = run("Austin, TX")
check(code == 0 and b, f"stay run exit {code}")
check(b["location"]["label"] == "Austin, Texas, United States", f"the hint must pick Texas over Minnesota: {b['location']['label']}")
check(b["verdict"]["kind"] == "stay" and md.count("**Verdict:** stay") == 1, f"in range should be stay: {b['verdict']}")
fc = [c for c in calls if c[0] == "api.open-meteo.com"]
check(len(fc) == 1 and len(parse_qs(urlparse(fc[0][1]).query)["latitude"][0].split(",")) == 33, "one forecast call should carry here + 32 ring points")
nws = [c for c in calls if c[0] == "api.weather.gov"]
check(len(nws) == 1 and "point=30.2672,-97.7431" in nws[0][1] and nws[0][2].get("User-Agent"), f"NWS once for here, with a User-Agent: {nws}")
check(b["alerts"]["status"] == "ok" and "none active (NWS)" in md, "no alerts should read 'none active'")
reach = {p["slug"]: p for p in b["people"]["within_reach"]}
check(set(reach) == {"pat-example"} and reach["pat-example"]["want_to_see_by"] == "2026-10-12" and 20 <= reach["pat-example"]["miles"] <= 35,
      f"Pat (Bastrop, ~28 mi) should be within reach, Wren (Windsor CO) not: {b['people']}")
check("Pat Example (people/pat-example.md)" in md and "want to see by 2026-10-12" in md, "the brief should name Pat with want_to_see_by")
cache = json.loads((tree / "personal/nomad/_geocache.json").read_text())
check(cache.get("bastrop|tx", {}).get("lat") == 30.1105 and cache.get("austin|tx", {}).get("lat") == AUSTIN[0], f"geocache should hold Austin and Bastrop: {sorted(cache)}")
check(not any("Windsor" in c[1] for c in calls), "a cached city must not be geocoded again")
for k in ("name:", "type:", "lobe: personal", "description:", "generated:", "location:", "lat: 30.2672", "lon: -97.7431", "timezone: America/Chicago", "sources:"):
    check(k in md.split("\n---\n", 1)[0], f"frontmatter lacks {k}")
for sec in ("## Here", "## Alerts", "## Freeze", "## Candidates", "## People within reach"):
    check(sec in md, f"brief lacks {sec}")
check(len(b["here"]["days"]) == 3 and b["here"]["days"][0]["high"] == 80 and b["here"]["days"][0]["night_low"] == 55, f"here days: {b['here']['days']}")
r = subprocess.run([sys.executable, str(SETUP / "build-index.py")], env=env, capture_output=True, text=True, timeout=120)
check(json.loads((tree / "people/_geo.json").read_text())["people"][0]["pending"] is False, "after the brief cached Bastrop, build-index should place Pat offline")

# --- 2. out of range tomorrow, one in-range candidate east at 100 miles -> drive today; wind flagged, not decided
S["weather"] = east_only({"highs": [84, 92, 93, 93], "lows": [58, 70, 70, 70], "wind": [35, 10, 10, 10]})
code, b, md = run("Austin, TX")
check(code == 0, f"drive run exit {code}")
v = b["verdict"]
check(v["kind"] == "drive today" and v["direction"] == "east" and v["miles"] == 100, f"expected drive today east 100: {v}")
check(v["line"].startswith("drive today: east, 100 miles, about 2 h 00 min"), f"verdict line: {v['line']}")
check("wind 35 mph on the leg (flagged only" in v["line"], f"wind over the line should be flagged: {v['line']}")
check([c["direction"] for c in b["candidates"]] == ["east"] and b["candidates"][0]["timezone"] == "America/Chicago", f"candidates: {b['candidates']}")
check(len(b["no_candidate_directions"]) == 7, f"seven directions should have no in-range point: {b['no_candidate_directions']}")
check(len([c for c in calls if c[0] == "api.weather.gov"]) == 2, "alerts should be checked at here and at the chosen candidate")
check([p["slug"] for p in b["candidates"][0]["people"]] == ["pat-example"], f"Pat is within 100 mi of the east point: {b['candidates'][0]['people']}")
check("| east | 100 |" in md and "east (100 mi): Pat Example" in md, "the brief should list the east candidate and Pat with it")

# --- 3. out only on day three -> drive in the next couple of days
S["weather"] = east_only({"highs": [80, 80, 90, 90], "lows": [55, 55, 55, 55], "wind": [10, 10, 10, 10]})
code, b, md = run("Austin, TX")
check(b["verdict"]["kind"] == "drive in the next couple of days" and b["verdict"]["miles"] == 100, f"day-three heat: {b['verdict']}")

# --- 4. a severe alert overrides to wait
S["weather"] = east_only({"highs": [84, 92, 93, 93], "lows": [58, 70, 70, 70], "wind": [10, 10, 10, 10]})
S["alerts"] = {"30.2672,-97.7431": [{"event": "Tornado Warning", "severity": "Extreme", "headline": "Tornado Warning issued", "ends": "2026-10-02T15:00:00-05:00", "areaDesc": "Travis"}]}
code, b, md = run("Austin, TX")
check(b["verdict"]["kind"] == "wait" and b["verdict"]["line"].startswith("wait: Tornado Warning (Extreme) here; otherwise drive today: east, 100 miles"), f"severe alert: {b['verdict']['line']}")
check("Tornado Warning (Extreme)" in md.split("## Alerts", 1)[1], "the alert should be listed")
S["alerts"] = {}

# --- 5. nowhere in range -> wait
S["weather"] = lambda lat, lon: HOT
code, b, md = run("Austin, TX")
check(b["verdict"]["kind"] == "wait" and "no direction is in range within 200 miles" in b["verdict"]["line"] and not b["candidates"], f"no candidate: {b['verdict']}")

# --- 6. freeze tonight flagged regardless of the verdict
S["weather"] = lambda lat, lon: {"highs": [60, 62, 64, 64], "lows": [28, 40, 41, 41], "wind": [5, 5, 5, 5]}
code, b, md = run("30.2672,-97.7431")
check(not [c for c in calls if c[0] == "geocoding-api.open-meteo.com"], "a lat,lon argument must not be geocoded")
check(b["verdict"]["kind"] == "stay" and "freeze tonight (low 28°F)" in b["verdict"]["line"], f"freeze tonight: {b['verdict']['line']}")
check(b["freeze"]["tonight"]["freeze"] and not b["freeze"]["tomorrow_night"]["freeze"] and "tonight: low 28°F · FREEZE" in md, f"freeze section: {b['freeze']}")

# --- 7. outside the US -> alerts skipped with a note, NWS never called
S["weather"] = lambda lat, lon: COOL
code, b, md = run("Tropea")
check(code == 0 and b["location"]["label"] == "Tropea, Calabria, Italy", f"Tropea run: {code} {b and b['location']}")
check(b["alerts"]["status"] == "skipped" and "outside the US" in b["alerts"]["note"] and "skipped: outside the US" in md, f"alerts outside the US: {b['alerts']}")
check(not [c for c in calls if c[0] == "api.weather.gov"], "NWS must not be called outside the US")
check(b["location"]["timezone"] == "Europe/Rome" and "timezone: Europe/Rome" in md, "the timezone comes from the forecast response")

# --- 8. unknown location -> exit 2, no brief, no network
code, b, md = run()
check(code == 2 and b is None and not calls, f"unknown location: exit {code}, calls {len(calls)}")

# --- 9. forecast down -> exit 1, no brief
S["forecast_error"] = True
code, b, md = run("Austin, TX")
check(code == 1 and b is None and not md, f"forecast failure: exit {code}")
S["forecast_error"] = False

shutil.rmtree(T, ignore_errors=True)
print("test-nomad-brief: PASS (stay, drive today east 100, next couple of days, severe wait, no-candidate wait, freeze tonight, outside-US skip, people in reach, one forecast call, unknown and failed runs)")
