import json
from pathlib import Path

# These tests are lightweight logic checks; they don't spin up Streamlit.

def test_boosting_logic_example():
    # simulate two results with equal base score
    results = [
        {"score": 0.3, "document": {"file_path": "/tmp/a.md"}},
        {"score": 0.3, "document": {"file_path": "/tmp/b.md"}},
    ]
    manifest = {
        "files": {
            "/tmp/a.md": {"pedagogical_implications": True, "pedagogical_score": 12},
            "/tmp/b.md": {"pedagogical_implications": False}
        }
    }

    boost = 0.5
    files_meta = manifest["files"]
    for r in results:
        meta = files_meta.get(r["document"]["file_path"], {})
        adjusted = r["score"]
        if boost > 0 and meta.get("pedagogical_implications"):
            ped_score = meta.get("pedagogical_score", 0)
            norm = min(ped_score / 15.0, 1.0)
            adjusted += boost * norm
        r["adjusted_score"] = adjusted

    # Expect pedagogical doc ranks higher
    results.sort(key=lambda x: x.get("adjusted_score", x["score"]), reverse=True)
    assert results[0]["document"]["file_path"] == "/tmp/a.md"
    assert results[0]["adjusted_score"] > results[1]["adjusted_score"]
