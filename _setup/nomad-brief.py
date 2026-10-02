#!/usr/bin/env python3
"""
name: nomad-brief
type: command
description: The nomad daily brief for the personal-morning skill (step 2). For a city or "lat,lon" (default: personal/nomad/location.md): three days of highs, lows, wind, gusts and precipitation here; active NWS alerts (US only; outside it, skipped with a note); freeze tonight and tomorrow night; a ring of 32 sample points (8 directions x ring_miles) with each direction's nearest in-range point, its miles, estimated drive time and timezone; per candidate leg a wind advisory (wind and dust alerts by name at here and every ring point out to the candidate, max gust, crosswind for the leg's heading, calmest 4-hour window), never a verdict; people from people/_geo.json within reach of here and of each candidate; one computed verdict line. Before "Nomad season starts around <date>" in location.md: the here-section and alerts only, one forecast point, verdict "nomad season starts <date>; no drive verdict". Keyless: Open-Meteo geocoding and forecast, NWS alerts. Writes personal/nomad/brief-<date>.md and a .json beside it with the same data.
why: Routine 2 of the Phase 0 captures, "know whether today is a driving day"; weather and routing come from a script with real data, never from an MD instruction or a general sense of the region; the people overlay is the point [rec_0c571abb1d 2026-09-22]. Keyless until a source proves insufficient [gordon 2026-09-21].
reads: personal/nomad/thresholds.md (every number used here, cited there: overnight_low_max_f 60 and daytime_high_max_f 85 [rec_0c571abb1d 2026-09-22], freeze_f 32 [gordon 2026-09-30], wind_sustained_mph 30 (an advisory line, said against the crosswind, never decides) [gordon 2026-10-02], wind Plan A [gordon 2026-10-02], drive_speed_est_mph, reach_people_miles, candidate_people_miles, ring_miles [derived: v1 design 2026-10-01]); personal/nomad/location.md (the city when no argument; the nomad season start always); people/_geo.json (built by build-index.py); personal/nomad/_geocache.json; Open-Meteo geocoding-api.open-meteo.com/v1/search and api.open-meteo.com/v1/forecast; NWS api.weather.gov/alerts/active
writes: personal/nomad/brief-<YYYY-MM-DD>.md and .json (the location's local date; a re-run that day replaces both); personal/nomad/_geocache.json (generated; the location and pending people cities, misses cached too)
schedule: on demand (personal-morning requests it; args [<city or "lat,lon">]); exit 2 when the location is unknown or not a place, 1 when the forecast cannot be had (no brief written: "no fresh weather")
test: _setup/tests/nomad-brief/
"""
# A day here is its high plus the night after it (18:00 to 09:00 local, from the hourly forecast). Verdict (skill step 4):
# out of range today or tomorrow -> drive today; out only on day three -> drive in the next couple of days; else stay.
# A candidate is in range when tonight's low and the next two days are. Drive verdicts need an in-range candidate,
# else "wait"; a Severe or Extreme NWS alert here or on the candidate's leg overrides to "wait", unless it is a wind or
# dust alert: wind never sets the verdict, it is an advisory with the leg (thresholds.md, Plan A). Freeze tonight is
# said regardless. Before the nomad season starts (location.md) there is no verdict, no ring and no people.
from __future__ import annotations

import datetime as dt, json, math, os, re, sys, urllib.error, urllib.request
from pathlib import Path
from urllib.parse import urlencode

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from sancho_lib import tree_root, city_query, place_matches  # noqa: E402

GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
NWS_URL = "https://api.weather.gov/alerts/active"
UA = "Sancho-nomad-brief/1 (personal weather brief)"
EARTH_MI = 3958.8
DIRECTIONS = [("north", "N", 0), ("northeast", "NE", 45), ("east", "E", 90), ("southeast", "SE", 135),
              ("south", "S", 180), ("southwest", "SW", 225), ("west", "W", 270), ("northwest", "NW", 315)]
DAYS = 3
NIGHT = (18, 9)            # a night runs 18:00 local to 09:00 the next morning
SEVERE = {"Severe", "Extreme"}
WIND_ALERT = re.compile(r"\bwind\b(?!\s+chill)|\bdust\b", re.I)  # Wind Advisory, High Wind Warning, Blowing Dust...; not Wind Chill
DRIVE_HOURS = (6, 20)      # crosswind and the calmest window look at 06:00 to 20:00, here's local time
CALM_HOURS = 4
SEASON = re.compile(r"Nomad season starts around (\d{4}-\d{2}-\d{2})", re.I)
GEOCODE_PER_RUN = 25       # people cities geocoded per run at most; the rest wait for the next run
US_BOXES = [(24.3, 49.5, -125.0, -66.8), (51.0, 71.5, -180.0, -129.9), (18.8, 22.4, -160.6, -154.6), (17.8, 18.6, -67.4, -65.2)]
NEED = ("overnight_low_max_f", "daytime_high_max_f", "freeze_f", "wind_sustained_mph", "drive_speed_est_mph",
        "reach_people_miles", "candidate_people_miles", "ring_miles")


class Fail(Exception):
    def __init__(self, msg, code=1):
        super().__init__(msg); self.code = code


def _get(url: str, headers: dict | None = None, timeout: int = 30) -> bytes:
    """The one network door; tests replace it."""
    req = urllib.request.Request(url, headers=headers or {})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def get_json(url, headers=None):
    return json.loads(_get(url, {"User-Agent": UA, **(headers or {})}).decode("utf-8"))  # NWS refuses a request without one


def write_atomic(path: Path, text: str):
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, path)


# ---------- thresholds and geometry ----------
def _today() -> dt.date:
    """The Mac's date; tests replace it."""
    return dt.date.today()


def load_thresholds(root: Path) -> dict:
    p = root / "personal" / "nomad" / "thresholds.md"
    if not p.exists():
        raise Fail(f"{p.relative_to(root)} missing", 2)
    t = {}
    for ln in p.read_text(encoding="utf-8").splitlines():
        m = re.match(r"\|\s*([a-z_]+)\s*\|\s*([\d.,\s]+?)\s*\|", ln)
        if m:
            vals = [float(x) for x in m.group(2).split(",") if x.strip()]
            t[m.group(1)] = vals if m.group(1) == "ring_miles" else vals[0]
    missing = [k for k in NEED if k not in t]
    if missing:
        raise Fail(f"thresholds.md lacks {', '.join(missing)}", 2)
    t["ring_miles"] = sorted(int(x) for x in t["ring_miles"])
    return t


def destination(lat, lon, bearing, miles):
    d, th, p1, l1 = miles / EARTH_MI, math.radians(bearing), math.radians(lat), math.radians(lon)
    p2 = math.asin(math.sin(p1) * math.cos(d) + math.cos(p1) * math.sin(d) * math.cos(th))
    l2 = l1 + math.atan2(math.sin(th) * math.sin(d) * math.cos(p1), math.cos(d) - math.sin(p1) * math.sin(p2))
    return round(math.degrees(p2), 4), round((math.degrees(l2) + 540) % 360 - 180, 4)


def miles_between(a, b):
    p1, p2 = math.radians(a[0]), math.radians(b[0])
    dp, dl = p2 - p1, math.radians(b[1] - a[1])
    h = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * EARTH_MI * math.asin(math.sqrt(h))


def in_us_box(lat, lon):
    return any(a <= lat <= b and c <= lon <= d for a, b, c, d in US_BOXES)


def drive_text(minutes):
    return f"{minutes // 60} h {minutes % 60:02d} min"


# ---------- geocoding (cached; misses cached too) ----------
class Geo:
    def __init__(self, root: Path):
        self.path = root / "personal" / "nomad" / "_geocache.json"
        try:
            self.cache = json.loads(self.path.read_text(encoding="utf-8")) if self.path.exists() else {}
        except ValueError:
            self.cache = {}
        self.dirty, self.calls = False, 0

    def lookup(self, key, name, hint, budget=True):
        if key in self.cache:
            return self.cache[key]
        if budget and self.calls >= GEOCODE_PER_RUN:
            return None
        self.calls += 1
        data = get_json(GEOCODE_URL + "?" + urlencode({"name": name, "count": 10, "language": "en", "format": "json"}))
        res = data.get("results") or []
        is_place = lambda r: str(r.get("feature_code") or "PPL").startswith("PPL")  # a town, not a country or a region
        if hint:
            pick = next((r for r in res if is_place(r) and place_matches(hint, r)), None)
        else:
            pick = res[0] if res and is_place(res[0]) else None
        today = dt.date.today().isoformat()
        if pick:
            label = ", ".join(x for x in (pick.get("name"), pick.get("admin1"), pick.get("country")) if x)
            entry = {"lat": round(float(pick["latitude"]), 4), "lon": round(float(pick["longitude"]), 4), "label": label,
                     "country_code": str(pick.get("country_code") or "").upper(), "timezone": pick.get("timezone") or "", "at": today}
        else:
            entry = {"none": True, "at": today}
        self.cache[key] = entry; self.dirty = True
        return entry

    def save(self):
        if self.dirty:
            write_atomic(self.path, json.dumps(dict(sorted(self.cache.items())), indent=1, ensure_ascii=False) + "\n")


def location_from_file(root: Path) -> dict:
    p = root / "personal" / "nomad" / "location.md"
    vals = {}
    if p.exists():
        for ln in p.read_text(encoding="utf-8").splitlines():
            m = re.match(r"^(city|lat|lon):\s*(.*)$", ln.strip())
            if m and m.group(1) not in vals:
                vals[m.group(1)] = m.group(2).strip()
    return vals


def nomad_season(root: Path) -> str:
    """The season start from location.md ("Nomad season starts around YYYY-MM-DD"), or "" when unsaid."""
    p = root / "personal" / "nomad" / "location.md"
    m = SEASON.search(p.read_text(encoding="utf-8")) if p.exists() else None
    try:
        return dt.date.fromisoformat(m.group(1)).isoformat() if m else ""
    except ValueError:
        return ""


def resolve_location(root: Path, arg: str, geo: Geo) -> dict:
    src = "argument"
    if not arg.strip():
        vals, src = location_from_file(root), "personal/nomad/location.md"
        try:
            return {"label": f"{float(vals['lat']):.4f}, {float(vals['lon']):.4f}", "lat": float(vals["lat"]), "lon": float(vals["lon"]),
                    "country_code": "", "source": src}
        except (KeyError, ValueError):
            arg = vals.get("city", "")
    m = re.match(r"^\s*(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)\s*$", arg)
    if m:
        lat, lon = float(m.group(1)), float(m.group(2))
        if not (-90 <= lat <= 90 and -180 <= lon <= 180):
            raise Fail(f"{arg!r} is not a latitude,longitude", 2)
        return {"label": f"{lat:.4f}, {lon:.4f}", "lat": lat, "lon": lon, "country_code": "", "source": src}
    key, name, hint = city_query(arg)
    if key is None:
        raise Fail(f"location unknown ({src}: {arg.strip()[:80] or 'blank'}); give a city or \"lat,lon\"", 2)
    try:
        hit = geo.lookup(key, name, hint, budget=False)
    except (urllib.error.URLError, OSError, ValueError) as e:
        raise Fail(f"geocoding {name!r} failed: {e}")
    if not hit or hit.get("none"):
        raise Fail(f"the geocoder found no place for {arg.strip()!r}", 2)
    return {"label": hit["label"], "lat": hit["lat"], "lon": hit["lon"], "country_code": hit.get("country_code", ""), "source": src}


# ---------- forecast ----------
def forecast(points: list[tuple[float, float]]) -> list[dict]:
    q = {"latitude": ",".join(f"{p[0]:.4f}" for p in points), "longitude": ",".join(f"{p[1]:.4f}" for p in points),
         "daily": "temperature_2m_max,temperature_2m_min,wind_speed_10m_max,wind_gusts_10m_max,precipitation_sum",
         "hourly": "temperature_2m,wind_speed_10m,wind_direction_10m,wind_gusts_10m",
         "timezone": "auto", "forecast_days": DAYS + 1, "temperature_unit": "fahrenheit", "wind_speed_unit": "mph",
         "precipitation_unit": "inch"}
    try:
        data = get_json(FORECAST_URL + "?" + urlencode(q, safe=","))
    except (urllib.error.URLError, OSError, ValueError) as e:
        raise Fail(f"forecast failed: {e}")
    if isinstance(data, dict) and data.get("error"):
        raise Fail(f"forecast refused: {data.get('reason')}")
    data = data if isinstance(data, list) else [data]
    if len(data) != len(points):
        raise Fail(f"forecast returned {len(data)} locations for {len(points)} asked")
    return [summarize(d) for d in data]


def _r(v):
    return None if v is None else int(round(float(v)))


def summarize(d: dict) -> dict:
    daily, hourly = d.get("daily") or {}, d.get("hourly") or {}
    dates = list(daily.get("time") or [])
    pairs = [(t, v) for t, v in zip(hourly.get("time") or [], hourly.get("temperature_2m") or []) if v is not None]
    days = []
    for i, date in enumerate(dates[:DAYS]):
        col = lambda k, j=i: (list(daily.get(k) or []) + [None] * len(dates))[j]
        nxt = (dt.date.fromisoformat(date) + dt.timedelta(days=1)).isoformat()
        start, end = f"{date}T{NIGHT[0]:02d}:00", f"{nxt}T{NIGHT[1]:02d}:00"
        night = [v for t, v in pairs if start <= t < end]
        low = min(night) if night else col("temperature_2m_min", i + 1)  # no hourly: the next day's daily minimum
        precip = col("precipitation_sum")
        days.append({"date": date, "high": _r(col("temperature_2m_max")), "night_low": _r(low), "day_low": _r(col("temperature_2m_min")),
                     "wind_max_mph": _r(col("wind_speed_10m_max")), "gust_max_mph": _r(col("wind_gusts_10m_max")),
                     "precip_in": None if precip is None else round(float(precip), 2)})
    n = len(hourly.get("time") or [])
    hcol = lambda k: (list(hourly.get(k) or []) + [None] * n)[:n]
    hours = [{"t": t, "speed": s, "dir": w, "gust": g} for t, s, w, g in
             zip(hourly.get("time") or [], hcol("wind_speed_10m"), hcol("wind_direction_10m"), hcol("wind_gusts_10m"))]
    return {"timezone": d.get("timezone") or "", "tz_abbr": d.get("timezone_abbreviation") or "",
            "utc_offset": int(d.get("utc_offset_seconds") or 0), "days": days, "hours": hours}


def day_problems(day: dict, th: dict, high=True) -> list[str]:
    out = []
    if day["night_low"] is None or (high and day["high"] is None):
        return ["no forecast"]
    if high and day["high"] > th["daytime_high_max_f"]:
        out.append(f"high {day['high']} > {th['daytime_high_max_f']:g}")
    if day["night_low"] > th["overnight_low_max_f"]:
        out.append(f"low {day['night_low']} > {th['overnight_low_max_f']:g}")
    return out


def point_in_range(fc: dict, th: dict) -> bool:
    d = fc["days"]
    return len(d) >= 3 and not day_problems(d[0], th, high=False) and not day_problems(d[1], th) and not day_problems(d[2], th)


# ---------- alerts ----------
def alerts_at(lat, lon, us: bool) -> dict:
    if not us:
        return {"status": "skipped", "note": "outside the US; NWS alerts cover the US only", "items": []}
    try:
        data = get_json(f"{NWS_URL}?point={lat:.4f},{lon:.4f}", {"Accept": "application/geo+json"})
    except urllib.error.HTTPError as e:
        if e.code in (400, 404):
            return {"status": "skipped", "note": f"NWS does not cover this point (HTTP {e.code})", "items": []}
        return {"status": "unavailable", "note": f"NWS HTTP {e.code}", "items": []}
    except (urllib.error.URLError, OSError, ValueError) as e:
        return {"status": "unavailable", "note": f"NWS unreachable: {e}", "items": []}
    items = []
    for f in data.get("features") or []:
        p = f.get("properties") or {}
        items.append({"event": p.get("event") or "", "severity": p.get("severity") or "", "headline": p.get("headline") or "",
                      "onset": p.get("onset") or p.get("effective") or "", "ends": p.get("ends") or p.get("expires") or "",
                      "area": p.get("areaDesc") or ""})
    return {"status": "ok", "note": "", "items": items}


class Alerts:
    """NWS alerts per point, each point asked once a run; after one unavailable answer the rest are not asked."""
    def __init__(self):
        self.cache, self.down = {}, False

    def at(self, pt, us: bool) -> dict:
        if pt not in self.cache:
            if self.down:
                return {"status": "unavailable", "note": "NWS not asked after an earlier failure", "items": []}
            self.cache[pt] = alerts_at(*pt, us)
            self.down = self.cache[pt]["status"] == "unavailable"
        return self.cache[pt]


def is_wind(a: dict) -> bool:
    return bool(WIND_ALERT.search(a.get("event") or ""))


def leg_alerts(c: dict, here_alerts: dict, nws: Alerts) -> dict:
    """Alerts here and at every ring point out to the candidate on its heading; one alert seen at two points is kept once."""
    items, statuses = [{**a, "where": "here"} for a in here_alerts["items"]], [here_alerts["status"]]
    for mi, pt, _ in c["_leg"]:
        a = nws.at(pt, in_us_box(*pt))
        statuses.append(a["status"])
        items += [{**x, "where": f"{mi} mi {c['direction']}"} for x in a["items"]]
    uniq = {}
    for x in items:
        uniq.setdefault((x["event"], x["headline"]), x)
    status = "unavailable" if "unavailable" in statuses else "skipped" if all(s == "skipped" for s in statuses) else "ok"
    return {"status": status, "items": list(uniq.values())}


# ---------- wind (Plan A: an advisory with the leg, never the verdict) ----------
def leg_wind(here: dict, c: dict, day: int) -> dict:
    """Sustained, gusts, crosswind for the leg's heading and the calmest window, over here and the leg's ring points."""
    fcs = [here] + [fc for _, _, fc in c["_leg"]]
    date = here["days"][day]["date"]
    pick = lambda k: [f["days"][day][k] for f in fcs if len(f["days"]) > day and f["days"][day].get(k) is not None]
    by_hour = {}
    for f in fcs:
        shift = dt.timedelta(seconds=here["utc_offset"] - f["utc_offset"])  # a leg across a timezone line, in here's hours
        for h in f["hours"]:
            t = dt.datetime.fromisoformat(h["t"]) + shift
            if t.date().isoformat() == date and DRIVE_HOURS[0] <= t.hour < DRIVE_HOURS[1]:
                by_hour.setdefault(t.hour, []).append(h)
    # wind_direction_10m is where the wind comes from; across the heading is speed x |sin(from - heading)|
    cross = [float(h["speed"]) * abs(math.sin(math.radians(float(h["dir"]) - c["bearing"])))
             for hs in by_hour.values() for h in hs if h["speed"] is not None and h["dir"] is not None]
    windows = []
    for start in range(DRIVE_HOURS[0], DRIVE_HOURS[1] - CALM_HOURS + 1):
        span = range(start, start + CALM_HOURS)
        g = [float(h["gust"]) for hr in span for h in by_hour.get(hr, []) if h["gust"] is not None]
        if g and all(by_hour.get(hr) for hr in span):
            windows.append((max(g), start))
    calm = min(windows) if windows else None  # the lowest worst gust; a tie goes to the earlier window
    return {"date": date, "bearing": c["bearing"], "alerts": [a for a in c["leg_alerts"]["items"] if is_wind(a)],
            "sustained_max_mph": max(pick("wind_max_mph"), default=None), "gust_max_mph": max(pick("gust_max_mph"), default=None),
            "crosswind_max_mph": _r(max(cross)) if cross else None,
            "calmest": {"from": calm[1], "to": calm[1] + CALM_HOURS, "gust_max_mph": _r(calm[0])} if calm else None}


def hour_text(h: int) -> str:
    return f"{h % 12 or 12}{'am' if h % 24 < 12 else 'pm'}"


def wind_text(w: dict, th: dict) -> str:
    parts = [f"{a['event']} ({a['where']})" for a in w["alerts"]]
    if w["gust_max_mph"] is not None:
        parts.append(f"gusts to {w['gust_max_mph']} mph" + (f" (sustained {w['sustained_max_mph']})" if w["sustained_max_mph"] is not None else ""))
    if w["crosswind_max_mph"] is not None:
        over = w["crosswind_max_mph"] >= th["wind_sustained_mph"]
        parts.append(f"crosswind up to {w['crosswind_max_mph']} mph" + (f", over the {th['wind_sustained_mph']:g} mph advisory line" if over else ""))
    if w["calmest"]:
        k = w["calmest"]
        parts.append(f"calmest {hour_text(k['from'])} to {hour_text(k['to'])} (gusts to {k['gust_max_mph']} mph)")
    return f"wind {dayname(w['date'])}: " + (", ".join(parts) or "no wind forecast")


# ---------- people ----------
def load_people(root: Path, geo: Geo) -> tuple[list[dict], str]:
    p = root / "people" / "_geo.json"
    if not p.exists():
        return [], "people/_geo.json not built yet (index.build writes it)"
    try:
        rows = json.loads(p.read_text(encoding="utf-8")).get("people") or []
    except ValueError:
        return [], "people/_geo.json unreadable"
    placed, waiting, offline = [], 0, False
    for r in rows:
        if r.get("lat") is None and r.get("query") and not offline:
            key, name, hint = city_query(r.get("city"))
            try:
                hit = geo.lookup(key, name, hint) if key else None
            except (urllib.error.URLError, OSError, ValueError):
                hit, offline = None, True
            if hit and not hit.get("none"):
                r = {**r, "lat": hit["lat"], "lon": hit["lon"], "resolved": hit["label"], "pending": False}
        if r.get("lat") is None:
            waiting += 1; continue
        placed.append(r)
    return placed, (f"{waiting} people with a city not placed yet" if waiting else "")


def person_line(r: dict, miles: float) -> dict:
    return {"slug": r["slug"], "name": r.get("name") or r["slug"], "city": r.get("city", ""), "resolved": r.get("resolved", ""),
            "miles": int(round(miles)), "want_to_see_by": r.get("want_to_see_by", ""), "last_seen": r.get("last_seen", "")}


# ---------- the brief ----------
def build(root: Path, arg: str) -> dict:
    th = load_thresholds(root)
    season = nomad_season(root)
    geo = Geo(root)
    try:
        loc = resolve_location(root, arg, geo)
        here_pt = (loc["lat"], loc["lon"])
        # Pre-season is judged on here's date below; the ring is left out only when the Mac's date puts the start more than
        # two days off, which no timezone gap reaches, so a pre-season morning costs one forecast point, not 33.
        want_ring = not season or _today() >= dt.date.fromisoformat(season) - dt.timedelta(days=2)
        ring = [(name, abbr, brg, mi, destination(loc["lat"], loc["lon"], brg, mi))
                for name, abbr, brg in DIRECTIONS for mi in th["ring_miles"]] if want_ring else []
        fcs = forecast([here_pt] + [r[4] for r in ring])
        here = fcs[0]
        if len(here["days"]) < DAYS:
            raise Fail(f"forecast has {len(here['days'])} days, need {DAYS}")
        for d in here["days"]:
            d["out"] = day_problems(d, th)
        us = loc["country_code"] == "US" if loc["country_code"] else in_us_box(*here_pt)
        nws = Alerts()
        alerts = nws.at(here_pt, us)
        head = {"generated": dt.datetime.now().astimezone().isoformat(timespec="seconds"), "date": here["days"][0]["date"],
                "location": {**loc, "timezone": here["timezone"], "tz_abbr": here["tz_abbr"]}, "season": {"starts": season},
                "thresholds": th, "here": {k: v for k, v in here.items() if k != "hours"}, "alerts": alerts}
        nws_src = "NWS alerts" if alerts["status"] == "ok" else f"NWS alerts ({alerts['status']})"
        if season and head["date"] < season:
            head["season"]["active"] = False
            line = f"nomad season starts {season}; no drive verdict"
            return {**head, "verdict": {"kind": "pre-season", "why": line, "direction": "", "miles": None, "drive_min": None, "flags": [], "line": line},
                    "sources": ["Open-Meteo geocoding", "Open-Meteo forecast", nws_src, "personal/nomad/location.md (season)"]}
        head["season"]["active"] = True

        speed = th["drive_speed_est_mph"]
        cands, dry = [], []
        for name, abbr, brg in DIRECTIONS:
            line = [(mi, pt, fc) for (n, _, _, mi, pt), fc in zip(ring, fcs[1:]) if n == name]
            best = next(((mi, pt, fc) for mi, pt, fc in line if point_in_range(fc, th)), None)
            if not best:
                dry.append(abbr); continue
            mi, pt, fc = best
            cands.append({"direction": name, "abbr": abbr, "bearing": brg, "miles": mi, "lat": pt[0], "lon": pt[1],
                          "drive_min": int(round(mi / speed * 60)), "timezone": fc["timezone"], "tz_abbr": fc["tz_abbr"], "days": fc["days"],
                          "_leg": [x for x in line if x[0] <= mi]})
        coolest = lambda c: max(d["high"] for d in c["days"][1:DAYS])
        cands.sort(key=lambda c: (c["miles"], coolest(c), c["bearing"]))
        d = here["days"]
        leg_day = 0 if d[0]["out"] or d[1]["out"] else 1  # the day the leg would be driven: today on a drive-today verdict
        for c in cands:
            c["leg_alerts"] = leg_alerts(c, alerts, nws)
            c["wind"] = leg_wind(here, c, leg_day)
            del c["_leg"]

        people, people_note = load_people(root, geo)
        reach = sorted((person_line(r, miles_between(here_pt, (r["lat"], r["lon"]))) for r in people
                        if miles_between(here_pt, (r["lat"], r["lon"])) <= th["reach_people_miles"]), key=lambda x: x["miles"])
        for c in cands:
            c["people"] = sorted((person_line(r, miles_between((c["lat"], c["lon"]), (r["lat"], r["lon"]))) for r in people
                                  if miles_between((c["lat"], c["lon"]), (r["lat"], r["lon"])) <= th["candidate_people_miles"]), key=lambda x: x["miles"])
    finally:
        geo.save()

    freeze = {"line_f": th["freeze_f"], "tonight": {"low": here["days"][0]["night_low"]}, "tomorrow_night": {"low": here["days"][1]["night_low"]}}
    for k in ("tonight", "tomorrow_night"):
        lo = freeze[k]["low"]
        freeze[k]["freeze"] = lo is not None and lo <= th["freeze_f"]

    return {**head, "freeze": freeze, "candidates": cands, "no_candidate_directions": dry,
            "people": {"within_reach": reach, "note": people_note}, "verdict": decide(here, cands, alerts, th, freeze),
            "sources": ["Open-Meteo geocoding", "Open-Meteo forecast", nws_src, "people/_geo.json", "personal/nomad/thresholds.md"]}


def dayname(date: str) -> str:
    return dt.date.fromisoformat(date).strftime("%a %m-%d")


def decide(here, cands, alerts, th, freeze) -> dict:
    d = here["days"]
    if any("no forecast" in x["out"] for x in d):
        v = {"kind": "wait", "why": "the forecast here is incomplete", "direction": "", "miles": None, "drive_min": None, "flags": []}
        v["line"] = f"wait: {v['why']}"
        return v
    if d[0]["out"] or d[1]["out"]:
        kind, when = "drive today", ("today" if d[0]["out"] else "tomorrow")
        why = f"{when} {', '.join(d[0]['out'] or d[1]['out'])} here"
    elif d[2]["out"]:
        kind, why = "drive in the next couple of days", f"{dayname(d[2]['date'])} {', '.join(d[2]['out'])} here"
    else:
        kind, why = "stay", f"in range here through {dayname(d[2]['date'])}"
    v = {"kind": kind, "why": why, "direction": "", "miles": None, "drive_min": None, "flags": []}
    if kind != "stay":
        if not cands:
            v.update(kind="wait", why=f"{why}, and no direction is in range within {th['ring_miles'][-1]} miles")
        else:
            c = cands[0]
            v.update(direction=c["direction"], miles=c["miles"], drive_min=c["drive_min"])
            severe = [a for a in c["leg_alerts"]["items"] if a["severity"] in SEVERE and not is_wind(a)]
            if severe:
                a = severe[0]
                where = "here" if a["where"] == "here" else f"on the leg, {a['where']}"
                v.update(kind="wait", why=f"{a['event']} ({a['severity']}) {where}; otherwise {kind}: {c['direction']}, {c['miles']} miles ({why})")
            v["flags"].append(wind_text(c["wind"], th))
            if c["leg_alerts"]["status"] == "unavailable" and alerts["status"] != "unavailable":
                v["flags"].append("alerts unavailable on part of the leg")
    if freeze["tonight"]["freeze"]:
        v["flags"].append(f"freeze tonight (low {freeze['tonight']['low']}°F)")
    if freeze["tomorrow_night"]["freeze"]:
        v["flags"].append(f"freeze tomorrow night (low {freeze['tomorrow_night']['low']}°F)")
    if alerts["status"] == "unavailable":
        v["flags"].append("alerts unavailable, severe weather not checked")
    head = v["kind"]
    if v["kind"] in ("drive today", "drive in the next couple of days"):
        head += f": {v['direction']}, {v['miles']} miles, about {drive_text(v['drive_min'])} ({v['why']})"
    else:
        head += f": {v['why']}"
    v["line"] = head + "".join(f"; {f}" for f in v["flags"])
    return v


def render(b: dict) -> str:
    loc, th, here = b["location"], b["thresholds"], b["here"]
    pre = b["verdict"]["kind"] == "pre-season"
    what = "Weather and alerts (nomad season not started)" if pre else "Weather, alerts, freeze, in-range directions, wind on the legs and people within reach"
    fm = ["---", f"name: Nomad brief {b['date']}", "type: brief", "lobe: personal",
          f"description: {what} for {loc['label']} on {b['date']}; written by nomad.brief, never by hand",
          f"generated: {b['generated']}", f"location: {json.dumps(loc['label'], ensure_ascii=False)}", f"lat: {loc['lat']}", f"lon: {loc['lon']}",
          f"timezone: {loc['timezone']}", "sources: [" + ", ".join(json.dumps(s) for s in b["sources"]) + "]", "---"]
    out = fm + [f"# Nomad brief · {loc['label']} · {b['date']}", "", f"**Verdict:** {b['verdict']['line']}", "",
                f"## Here ({loc['timezone']}{', ' + loc['tz_abbr'] if loc['tz_abbr'] else ''})",
                "| day | high °F | night low °F | wind max | gusts | precip | range |", "|---|---|---|---|---|---|---|"]
    for d in here["days"]:
        out.append(f"| {dayname(d['date'])} | {d['high']} | {d['night_low']} | {d['wind_max_mph']} mph | {d['gust_max_mph']} mph | {d['precip_in']} in | {'; '.join(d['out']) or 'in'} |")
    out += ["", "## Alerts"]
    a = b["alerts"]
    if a["status"] != "ok":
        out.append(f"- {a['status']}: {a['note']}")
    elif not a["items"]:
        out.append("- none active (NWS)")
    else:
        out += [f"- {x['event']} ({x['severity']}), until {x['ends'] or '?'}: {x['headline']}" for x in a["items"]]
    if pre:
        return "\n".join(out) + "\n"
    leg = {}
    for c in b["candidates"]:
        for x in c["leg_alerts"]["items"]:
            if x["where"] != "here":
                leg.setdefault((x["event"], x["headline"]), x)
    out += [f"- on the legs: {x['event']} ({x['severity']}), {x['where']}, until {x['ends'] or '?'}: {x['headline']}" for x in leg.values()]
    f = b["freeze"]
    out += ["", f"## Freeze (line {f['line_f']:g}°F)"]
    for k, label in (("tonight", "tonight"), ("tomorrow_night", "tomorrow night")):
        out.append(f"- {label}: low {f[k]['low']}°F{' · FREEZE' if f[k]['freeze'] else ''}")
    out += ["", f"## Candidates (nearest in-range point per direction; straight-line miles, drive at {th['drive_speed_est_mph']:g} mph)"]
    if b["candidates"]:
        out += ["| direction | miles | highs °F | lows °F | est. drive | timezone |", "|---|---|---|---|---|---|"]
        for c in b["candidates"]:
            hi = "/".join(str(d["high"]) for d in c["days"]); lo = "/".join(str(d["night_low"]) for d in c["days"])
            out.append(f"| {c['direction']} | {c['miles']} | {hi} | {lo} | {drive_text(c['drive_min'])} | {c['timezone']} |")
    else:
        out.append(f"- none in range within {th['ring_miles'][-1]} miles")
    if b["no_candidate_directions"]:
        out.append(f"- no in-range point: {', '.join(b['no_candidate_directions'])}")
    if b["candidates"]:
        out += ["", f"## Wind on the legs (advisory, never the verdict; crosswind and calmest window {hour_text(DRIVE_HOURS[0])} to {hour_text(DRIVE_HOURS[1])})"]
        out += [f"- {c['direction']} ({c['miles']} mi, heading {c['bearing']}°): {wind_text(c['wind'], th)}" for c in b["candidates"]]
    out += ["", f"## People within reach ({th['reach_people_miles']:g} miles of here; {th['candidate_people_miles']:g} of a candidate)"]
    pl = lambda p: f"{p['name']} (people/{p['slug']}.md), {p['resolved'] or p['city']}, {p['miles']} mi" + \
        (f", want to see by {p['want_to_see_by']}" if p["want_to_see_by"] else "") + (f", last seen {p['last_seen']}" if p["last_seen"] else "")
    out += [f"- here: {pl(p)}" for p in b["people"]["within_reach"]] or ["- here: nobody placed within reach"]
    for c in b["candidates"]:
        out += [f"- {c['direction']} ({c['miles']} mi): {pl(p)}" for p in c["people"]]
    if b["people"]["note"]:
        out.append(f"- note: {b['people']['note']}")
    return "\n".join(out) + "\n"


def main(argv: list[str]) -> int:
    root = tree_root()
    try:
        b = build(root, " ".join(argv))
    except Fail as e:
        print(f"nomad.brief: FAIL: {e}"); return e.code
    folder = root / "personal" / "nomad"
    md, js = folder / f"brief-{b['date']}.md", folder / f"brief-{b['date']}.json"
    write_atomic(js, json.dumps(b, indent=1, ensure_ascii=False) + "\n")
    write_atomic(md, render(b))
    print(f"nomad.brief: {md.relative_to(root)} · {b['verdict']['line']}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
