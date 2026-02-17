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

    INDEX_PATH.parent.mkdir(exist_ok=True)
    INDEX_PATH.write_text(json.dumps(records, indent=2), encoding="utf-8")

    print(f"Indexed {len(records)} items into {INDEX_PATH}")

if __name__ == "__main__":
    index_kb()
