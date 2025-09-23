#!/usr/bin/env python3
import sys, csv
from collections import defaultdict

PATH = sys.argv[1] if len(sys.argv) > 1 else \
    "/Users/simonwang/Documents/Usage/VibeCoding/letter_writing/data_archive/hko_wind_data_20250907_224309-937.csv"

SIG3 = 41.0
SIG8 = 63.0

by_ts = defaultdict(list)
with open(PATH, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        ts = row.get('timestamp_hkt') or row.get('timestamp_utc') or ''
        try:
            sp = row.get('wind_speed_kmh')
            speed = float(sp) if sp not in (None, '', 'null') else None
        except Exception:
            speed = None
        if speed is not None:
            by_ts[ts].append(speed)

summary = []
for ts, speeds in sorted(by_ts.items()):
    total = len(speeds)
    s3 = sum(1 for v in speeds if v >= SIG3)
    s8 = sum(1 for v in speeds if v >= SIG8)
    calc = 8 if s8 >= (total/2) else 3 if s3 >= (total/2) else 1
    summary.append((ts, total, s3, s8, calc))

print(f"Timestamps: {len(summary)}")
for ts, total, s3, s8, calc in summary:
    print(f"{ts}: total={total}, >=41={s3}, >=63={s8}, calc={calc}")
