import shutil
from pathlib import Path
import frontmatter
import yaml

def render_document(record, output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)

    doc_path = Path(record["path"])
    doc_type = record["type"]

    # BINARY DOCUMENT (PDF, DOCX)
    if doc_type == "binary":
        target = output_dir / doc_path.name
        shutil.copy2(doc_path, target)
        return {
            "type": "binary",
            "output": str(target),
            "title": record["metadata"].get("title", doc_path.stem)
        }
    
    # MARKDOWN (handled later)
    if doc_type == "markdown":
        meta, content = frontmatter.load(doc_path).metadata, frontmatter.load(doc_path).content
        out_path = output_dir / (doc_path.stem + ".md")
        out_path.write_text(content, encoding="utf-8")
        return {
            "type": "markdown",
            "output": str(out_path),
            "title": meta.get("title", doc_path.stem)
        }
    
    raise ValueError(f"Unknown document type: {doc_type}")

