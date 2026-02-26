# src/docfetcher/indexer.py
"""
 * Project:        KnowMore
 * File:           indexer.py
 * Description:    Document indexing functions for the KnowMore document fetcher application
 * Author:         Josh Cross
 * Created:        18/02/2026
 * Last Modified:  18/02/2026 by Josh Cross
 *
""" 

import yaml
from pathlib import Path
import json

KB_ROOT = Path(__file__).resolve().parents[2] / "kb"
INDEX_PATH = Path(__file__).resolve().parents[2] / "data" / "index.json"

SUPPORTED_DOCS = {".md", ".pdf", ".docx", ".txt"}

def load_sidecar_metadata(file_path: Path):
    meta_path = file_path.with_suffix(file_path.suffix + ".meta.yaml")
    if meta_path.exists():
        try:
            data = yaml.safe_load(meta_path.read_text(encoding="utf-8")) or {}
            if not isinstance(data, dict):
                return {}
            return data
        except Exception:
            return {}
    return {}

def make_json_safe(obj):
    if isinstance(obj, dict):
        return {k: make_json_safe(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [make_json_safe(v) for v in obj]
    if isinstance(obj, (int, float, str, bool)) or obj is None:
        return obj
    return str(obj)

def load_md_frontmatter(md_path: Path) -> dict:
    text = md_path.read_text(encoding="utf-8", errors="replace")
    if not text.lstrip().startswith("---"):
        return {}
    # Find the closing --- line
    lines = text.splitlines()
    if len(lines) < 3:
        return {}
    if lines[0].strip() != "---":
        return {}
    # Find end marker
    end_idx = None
    for i in range(1, min(len(lines), 200)):  # limit scan
        if lines[i].strip() == "---":
            end_idx = i
            break
    if end_idx is None:
        return {}
    yaml_block = "\n".join(lines[1:end_idx])
    try:
        data = yaml.safe_load(yaml_block) or {}
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}

def index_kb():
    records = []

    for file in KB_ROOT.rglob("*"):
        if not file.is_file():
            continue

        ext = file.suffix.lower()

        if ext == ".md":
            fm = load_md_frontmatter(file)
            records.append({
                "type": "markdown",
                "path": str(file),
                "metadata": fm or {},
            })
            continue

        if ext in SUPPORTED_DOCS:
            meta = load_sidecar_metadata(file)
            records.append({
                "type": "binary",
                "path": str(file),
                "metadata": meta if isinstance(meta, dict) else {},
            })
            continue

    safe_records = make_json_safe(records)
    INDEX_PATH.parent.mkdir(exist_ok=True)
    INDEX_PATH.write_text(json.dumps(safe_records, indent=2), encoding="utf-8")
    print(f"Indexed {len(records)} items into {INDEX_PATH}")

if __name__ == "__main__":
    index_kb()