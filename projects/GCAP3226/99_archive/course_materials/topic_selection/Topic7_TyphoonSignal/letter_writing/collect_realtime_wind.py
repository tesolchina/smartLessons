#!/usr/bin/env python3
"""
Lightweight background collector for Hong Kong Observatory real-time 10-minute wind data.
- Polls the HKO WFS endpoint to list stations and their CSV Data_url
- Fetches each station's CSV and extracts the most recent wind speed/gust when possible
- Appends consolidated rows into a daily CSV log to avoid missing updates

Usage examples:
  - One-off test run:
      python collect_realtime_wind.py --once
  - Continuous run every 60s:
      python collect_realtime_wind.py --interval 60

Output:
  - data_archive/hk_wind_log_YYYYMMDD.csv

Columns:
  timestamp_utc, timestamp_hkt, station_name, latitude, longitude, wind_speed_kmh, wind_gust_kmh, data_url, official_signal_hko

Notes:
  - This script is resilient to individual station failures and network hiccups.
  - Designed for long-running background use; consider launchd (macOS) or nohup.
"""

from __future__ import annotations
import argparse
import csv
import os
import signal
import sys
import time
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional, Tuple

import requests
import csv as _csv

WFS_URL = (
    "https://portal.csdi.gov.hk/server/services/common/"
    "hko_rcd_1634953844424_88011/MapServer/WFSServer?service=wfs"
    "&request=GetFeature&typenames=latest_10min_wind&outputFormat=geojson"
)
HKO_WARN_URL = (
    "https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=warnsum&lang=en"
)

STOP = False

def _handle_sigterm(signum, frame):
    global STOP
    STOP = True


def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)


def iso_now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def hkt_now() -> datetime:
    return datetime.now(timezone.utc) + timedelta(hours=8)


def get_official_signal() -> int:
    try:
        r = requests.get(HKO_WARN_URL, timeout=15)
        r.raise_for_status()
        data = r.json()
        sig = 1
        if "WTCSGNL" in data:
            w = data["WTCSGNL"]
            t = (w.get("type") or "").upper()
            c = (w.get("code") or "").upper()
            if "10" in t or "TC10" in c:
                sig = 10
            elif "9" in t or "TC9" in c:
                sig = 9
            elif "8" in t or "TC8" in c:
                sig = 8
            elif "3" in t or "TC3" in c:
                sig = 3
            elif "1" in t or "TC1" in c:
                sig = 1
        return sig
    except Exception:
        return -1


def fetch_stations() -> List[Dict]:
    r = requests.get(WFS_URL, timeout=30)
    r.raise_for_status()
    gj = r.json()
    stations = []
    for feat in gj.get("features", []):
        props = feat.get("properties", {})
        geom = feat.get("geometry", {})
        coords = (geom.get("coordinates") or [None, None])
        stations.append(
            {
                "station_name": props.get("AutomaticWeatherStation_en") or "Unknown",
                "longitude": coords[0],
                "latitude": coords[1],
                "data_url": props.get("Data_url") or "",
            }
        )
    return stations


def parse_station_csv_latest(csv_text: str) -> Dict[str, Optional[float]]:
    """Parse the station CSV text and extract the latest 10-min mean speed and gust.

    HKO schema (first language block):
      0..6 = Y, M, D, H, Min, Sec, TZ
      7    = Automatic Weather Station (name)
      8    = 10-Minute Mean Wind Direction (Compass points)
      9    = 10-Minute Mean Speed (km/h)
      10   = 10-Minute Maximum Gust (km/h)
    The file repeats the block for other languages; we always target the first block.
    """
    try:
        # Use csv.reader for robust parsing (avoids mis-splitting on commas)
        rows = [r for r in _csv.reader(csv_text.splitlines()) if r]
        if len(rows) < 2:
            return {"wind_speed": None, "wind_gust": None}
        last = rows[-1]
        wind_speed: Optional[float] = None
        wind_gust: Optional[float] = None
        # Fast path: exact positions
        try:
            if len(last) >= 11:
                sp = last[9].strip()
                gs = last[10].strip()
                speed_val = float(sp) if sp != "" else None
                gust_val = float(gs) if gs != "" else None
                if speed_val is not None and 0 <= speed_val <= 200:
                    wind_speed = speed_val
                    if gust_val is not None and 0 <= gust_val <= 300:
                        wind_gust = gust_val
                    else:
                        wind_gust = round(wind_speed * 1.3, 1)
        except Exception:
            # ignore and fallback
            pass
        # Fallback heuristic if fast-path failed
        if wind_speed is None:
            for cell in last[5:]:
                try:
                    v = float(cell)
                except Exception:
                    continue
                if 0 <= v <= 200 and wind_speed is None:
                    wind_speed = v
                elif wind_speed is not None and wind_gust is None and 0 <= v <= 300 and v >= wind_speed:
                    wind_gust = v
                    break
            if wind_speed is not None and wind_gust is None:
                wind_gust = round(wind_speed * 1.3, 1)
        return {"wind_speed": wind_speed, "wind_gust": wind_gust}
    except Exception:
        return {"wind_speed": None, "wind_gust": None}


def _suspicious_uniform_pattern(speeds: List[Optional[float]], gusts: List[Optional[float]]) -> Tuple[bool, str]:
    """Detect likely parsing artifact (e.g., uniform 9.0 speeds across many stations).

    Returns (is_suspicious, reason)
    """
    vals = [v for v in speeds if isinstance(v, (int, float))]
    if not vals:
        return (False, "")
    n = len(vals)
    # Majority equal to a single low value (<= 10 km/h)
    from collections import Counter
    c = Counter(round(v, 1) for v in vals)
    value, count = c.most_common(1)[0]
    low_majority = value <= 10 and count >= max(5, int(0.6 * n))
    # Gusts also share a small set like {10, 20, 40}
    gvals = [g for g in gusts if isinstance(g, (int, float))]
    gset = set(round(g, 1) for g in gvals)
    gust_repetitive = len(gset) <= 3 and all(g <= 50 for g in gset) if gvals else False
    if low_majority and gust_repetitive:
        return (True, f"uniform value {value} across {count}/{n} stations; gust set={sorted(gset)}")
    if low_majority:
        return (True, f"uniform value {value} across {count}/{n} stations")
    return (False, "")


def write_row(writer, row: List):
    writer.writerow(row)


def collector_once(out_dir: str, station_limit: Optional[int] = None) -> int:
    ensure_dir(out_dir)
    ts_utc = iso_now_utc()
    ts_hkt = hkt_now().strftime("%Y-%m-%dT%H:%M:%S+08:00")
    ymd = datetime.now().strftime("%Y%m%d")
    out_path = os.path.join(out_dir, f"hk_wind_log_{ymd}.csv")
    new_file = not os.path.exists(out_path)

    official = get_official_signal()

    try:
        stations = fetch_stations()
    except Exception as e:
        # Still write a heartbeat row so we know the collector is alive
        stations = []

    if station_limit is not None:
        stations = stations[: station_limit]

    count = 0
    with open(out_path, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if new_file:
            write_row(
                w,
                [
                    "timestamp_utc",
                    "timestamp_hkt",
                    "station_name",
                    "latitude",
                    "longitude",
                    "wind_speed_kmh",
                    "wind_gust_kmh",
                    "data_url",
                    "official_signal_hko",
                ],
            )
        if not stations:
            write_row(w, [ts_utc, ts_hkt, "<none>", "", "", "", "", "", official])
            return 1
        session = requests.Session()
        speeds_batch: List[Optional[float]] = []
        gusts_batch: List[Optional[float]] = []
        for st in stations:
            data_url = st.get("data_url") or ""
            wind_speed = None
            wind_gust = None
            if data_url:
                try:
                    resp = session.get(data_url, timeout=20)
                    resp.raise_for_status()
                    parsed = parse_station_csv_latest(resp.text)
                    wind_speed = parsed.get("wind_speed")
                    wind_gust = parsed.get("wind_gust")
                except Exception:
                    pass
            speeds_batch.append(wind_speed)
            gusts_batch.append(wind_gust)
            write_row(
                w,
                [
                    ts_utc,
                    ts_hkt,
                    st.get("station_name", ""),
                    st.get("latitude", ""),
                    st.get("longitude", ""),
                    wind_speed if wind_speed is not None else "",
                    wind_gust if wind_gust is not None else "",
                    data_url,
                    official,
                ],
            )
            count += 1
        # Post-batch sanity check for suspicious uniform low values
        suspicious, reason = _suspicious_uniform_pattern(speeds_batch, gusts_batch)
        if suspicious:
            try:
                log_path = os.path.join(out_dir, "collector.log")
                with open(log_path, "a", encoding="utf-8") as lf:
                    lf.write(f"{datetime.now().isoformat()} SUSPICIOUS_DATA {reason}\n")
            except Exception:
                pass
        # Always write a heartbeat so we can confirm the collector is alive
        try:
            log_path = os.path.join(out_dir, "collector.log")
            with open(log_path, "a", encoding="utf-8") as lf:
                lf.write(
                    f"{datetime.now().isoformat()} HEARTBEAT wrote_rows={count} file={out_path} official_signal={official}\n"
                )
        except Exception:
            pass
    return count


def main():
    parser = argparse.ArgumentParser(description="HKO real-time wind background collector")
    parser.add_argument("--interval", type=int, default=60, help="Polling interval in seconds (default: 60)")
    parser.add_argument("--out-dir", default="data_archive", help="Output directory (default: data_archive)")
    parser.add_argument("--station-limit", type=int, default=None, help="Limit number of stations (debug)")
    parser.add_argument("--once", action="store_true", help="Run one cycle and exit")
    args = parser.parse_args()

    signal.signal(signal.SIGINT, _handle_sigterm)
    signal.signal(signal.SIGTERM, _handle_sigterm)

    if args.once:
        n = collector_once(args.out_dir, args.station_limit)
        print(f"Wrote {n} station rows")
        return 0

    print(f"Starting collector: interval={args.interval}s, out_dir={args.out_dir}")
    while not STOP:
        try:
            n = collector_once(args.out_dir, args.station_limit)
            print(f"{datetime.now().isoformat()} wrote {n} station rows")
        except Exception as e:
            print(f"Collector cycle error: {e}")
        # Sleep in small chunks to react quicker to stop signal
        remaining = args.interval
        while remaining > 0 and not STOP:
            time.sleep(min(1, remaining))
            remaining -= 1
    print("Collector stopped")
    return 0


if __name__ == "__main__":
    sys.exit(main())
