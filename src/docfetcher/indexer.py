"""
 * Project:        KnowMore
 * File:           indexer.py
 * Description:    Document indexing functions for the KnowMore document fetcher application
 * Author:         Josh Cross
 * Created:        18/02/2026
 * Last Modified:  18/02/2026 by Josh Cross
 *
""" 

# Public modules
import yaml
from pathlib import Path
import json

"""   CONSTANTS  """
KB_ROOT = Path(__file__).resolve().parents[2] / "kb"
INDEX_PATH = Path(__file__).resolve().parents[2] / "data" / "index.json"

SUPPORTED_DOCS = {".md", ".pdf", ".docx"}

def load_sidecar_metadata(file_path: Path):
    # Loads .meta.yaml next to PDF/DOCX
    meta_path = file_path.with_suffix(file_path.suffix + ".meta.yaml")
    if meta_path.exists():
        return yaml.safe_load(meta_path.read_text(encoding="utf-8"))
    return {}

def make_json_safe(obj):
    if isinstance(obj, dict):
        return {k: make_json_safe(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [make_json_safe(v) for v in obj]
    if isinstance(obj, (int, float, str, bool)) or obj is None:
        return obj
    # Convert dates, datetimes, Path, etc. to strings
    return str(obj)

def index_kb():
    records = []

    for file in KB_ROOT.rglob("*"):
        if not file.is_file():
            continue

        ext = file.suffix.lower()

        # 1. Markdown docs -----------------------------------------
        if ext == ".md":
            # Load frontmatter later when needed
            records.append({
                "type": "markdown",
                "path": str(file),
                "metadata": {},  # will get populated on render
            })
            continue

        # 2. Binary docs with meta sidecars -------------------------
        if ext in SUPPORTED_DOCS:
            meta = load_sidecar_metadata(file)
            records.append({
                "type": "binary",
                "path": str(file),
                "metadata": meta,
            })
            continue

        # 3. Info files (.txt etc.) ignored at index level ----------

    safe_records = make_json_safe(records)
    INDEX_PATH.parent.mkdir(exist_ok=True)
    INDEX_PATH.write_text(json.dumps(safe_records, indent=2), encoding="utf-8")

    print(f"Indexed {len(records)} items into {INDEX_PATH}")

if __name__ == "__main__":
    index_kb()
