from __future__ import annotations
from pathlib import Path
import re
import time
import urllib.parse
import urllib.request
import json

BASE = Path("/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/projects/GCAP3226")
OUT_ROOT = BASE / "course_materials/resources/datasets/open_data"
OUT_ROOT.mkdir(parents=True, exist_ok=True)

CKAN_BASE = "https://data.gov.hk/en-data/api/3/action"
# Expanded multilingual keywords for higher recall
TOPICS = {
    "transport": [
        "transport", "traffic", "journey time", "speed map", "congestion", "td", "road",
        "交通", "運輸", "路線", "行車時間", "擁塞", "速度地圖"
    ],
    "air_quality": [
        "air quality", "aqhi", "pm2.5", "pm25", "pm10", "no2", "o3", "so2", "pollution", "lamppost",
        "空氣質素", "空氣污染", "空氣質素健康指數", "路燈", "監測"
    ],
    "housing": [
        "housing", "housing authority", "estate", "public housing", "waiting time", "waiting list", "allocation", "supply",
        "房屋", "公屋", "房屋署", "房委會", "輪候", "輪候冊", "編配", "供應"
    ],
}
PREFERRED_EXT = (".csv", ".json", ".geojson", ".xls", ".xlsx")


def ckan_request(action: str, params: dict) -> dict:
    url = f"{CKAN_BASE}/{action}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))

def search_packages_paged(q: str, max_rows: int = 100, page_rows: int = 25) -> list[dict]:
    """Paginate CKAN package_search to collect up to max_rows results."""
    results: list[dict] = []
    start = 0
    while len(results) < max_rows:
        rows = min(page_rows, max_rows - len(results))
        data = ckan_request("package_search", {"q": q, "rows": rows, "start": start})
        if not data.get("success"):
            break
        chunk = data["result"].get("results", [])
        if not chunk:
            break
        results.extend(chunk)
        start += len(chunk)
        if len(chunk) < rows:
            break
        time.sleep(0.3)
    return results


def pick_resources(pkg: dict) -> list[dict]:
    res = []
    for r in pkg.get("resources", []):
        url = r.get("url") or ""
        fmt = (r.get("format") or "").lower()
        ext = Path(urllib.parse.urlparse(url).path).suffix.lower()
        if ext in PREFERRED_EXT or fmt in {"csv", "json", "geojson"}:
            res.append({
                "name": r.get("name") or pkg.get("title"),
                "url": url,
                "format": fmt or (ext[1:] if ext else ""),
            })
    return res


def download(url: str, out_path: Path) -> bool:
    try:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=45) as resp, open(out_path, "wb") as f:
            f.write(resp.read())
        return True
    except Exception as e:
        print(f"  Download failed: {url}\n    -> {e}")
        return False

def safe_slug(text: str, max_len: int = 80) -> str:
    s = "".join([c if c.isalnum() or c in ("-", "_") else "_" for c in str(text)])
    return s[:max_len] if max_len else s

def load_existing_ok_urls(manifest_path: Path) -> set[str]:
    try:
        import pandas as pd
        if manifest_path.exists():
            mf = pd.read_csv(manifest_path)
            if "url" not in mf.columns:
                return set()
            status_col = mf["status"].astype(str) if "status" in mf.columns else pd.Series(["ok"] * len(mf))
            ok_mask = status_col.fillna("").str.lower() == "ok"
            ok = mf.loc[ok_mask, "url"].dropna().astype(str)
            return set(ok.tolist())
    except Exception:
        pass
    return set()


def fetch_topic(topic: str, keywords: list[str], limit_pkgs: int = 30, limit_res_per_pkg: int = 5, skip_urls: set[str] | None = None) -> list[dict]:
    fetched: list[dict] = []
    # Use a broad free-text query to improve recall
    q = " OR ".join(keywords)
    packages = search_packages_paged(q, max_rows=limit_pkgs, page_rows=25)
    for pkg in packages:
        title = str(pkg.get("title") or pkg.get("name") or "")
        org = str((pkg.get("organization") or {}).get("title") or (pkg.get("organization") or {}).get("name") or "")
        resources = pick_resources(pkg)[:limit_res_per_pkg]
        for r in resources:
            url = r["url"]
            if not url:
                continue
            if skip_urls and url in skip_urls:
                # Already fetched successfully before
                continue
            ext = Path(urllib.parse.urlparse(url).path).suffix.lower() or ".dat"
            safe_title = safe_slug(title, 80)
            safe_res = safe_slug(r.get("name") or "", 50)
            out_dir = OUT_ROOT / topic
            out_path = out_dir / f"{safe_title}__{safe_res}{ext}"
            if out_path.exists():
                # Skip re-download to save bandwidth
                fetched.append({
                    "topic": topic,
                    "package": title,
                    "resource": r["name"],
                    "provider": org,
                    "url": url,
                    "saved_to": str(out_path),
                    "status": "ok",
                })
                continue
            print(f"[{topic}] {title} — {r['name']}\n  -> {url}")
            ok = download(url, out_path)
            fetched.append({
                "topic": topic,
                "package": title,
                "resource": r["name"],
                "provider": org,
                "url": url,
                "saved_to": str(out_path),
                "status": "ok" if ok else "failed",
            })
            time.sleep(0.5)
    return fetched


def main():
    all_rows: list[dict] = []
    # Load existing manifest to avoid re-downloading already-successful URLs
    manifest_path = BASE / "_open_data_inventory/ckan_fetch_manifest.csv"
    skip_urls = load_existing_ok_urls(manifest_path)
    for topic, kws in TOPICS.items():
        # Fetch more broadly now
        rows = fetch_topic(topic, kws, limit_pkgs=80, limit_res_per_pkg=5, skip_urls=skip_urls)
        all_rows.extend(rows)
    # write manifest
    import pandas as pd
    out_csv = manifest_path
    new_mf = pd.DataFrame(all_rows)
    if out_csv.exists():
        try:
            old_mf = pd.read_csv(out_csv)
            mf = pd.concat([old_mf, new_mf], ignore_index=True)
            # Drop duplicate rows by URL + saved_to, keep the last (latest status)
            if {"url", "saved_to"}.issubset(mf.columns):
                mf = mf.drop_duplicates(subset=["url", "saved_to"], keep="last")
        except Exception:
            mf = new_mf
    else:
        mf = new_mf
    mf.to_csv(out_csv, index=False)
    if not mf.empty:
        print("\nManifest:")
        cols = [c for c in ["topic", "package", "resource", "status", "saved_to"] if c in mf.columns]
        print(mf[cols].head(20).to_string(index=False))
    else:
        print("No datasets fetched. Try refining keywords or increasing search rows.")


if __name__ == "__main__":
    main()
