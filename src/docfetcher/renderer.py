# src/docfetcher/renderer.py
"""
Project:        KnowMore
File:           renderer.py
Description:    Rendering/Exporting dispatcher for KnowMore records
Author:         Josh Cross
Created:        18/02/2026
Last Modified:  26/02/2026 by Josh Cross
"""

from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import streamlit as st
from typing import Literal, Optional, Dict, Any
import shutil

# UI helpers are intentionally imported here to keep UI widgets encapsulated,
# but the UI file should remain "thin" and only call these entry points.
from docfetcher.helpers import render_pdf, render_info

RenderKind = Literal["inline_pdf", "inline_text", "metadata", "none"]
ExportKind = Literal["binary", "text", "none"]

@dataclass
class RenderResult:
    kind: RenderKind
    # When kind == "inline_pdf", "inline_text", the renderer will handle UI drawing
    # and return any contextual info (optional).
    context: Optional[Dict[str, Any]] = None
    # For cases where we only want to show metadata
    metadata: Optional[Dict[str, Any]] = None
    # Path being rendered (for context)
    path: Optional[str] = None

@dataclass
class ExportResult:
    type: ExportKind
    output: Optional[str] = None
    message: Optional[str] = None

SUPPORTED_INLINE = {".pdf", ".txt"}       # file types we render inline today
SUPPORTED_EXPORT = {".pdf", ".md", ".docx", ".txt"}  # file types we can export as-is (v1)

def _is_pdf(path: Path) -> bool:
    return path.suffix.lower() == ".pdf"

def _is_text(path: Path) -> bool:
    return path.suffix.lower() == ".txt"

def _is_markdown(path: Path) -> bool:
    return path.suffix.lower() == ".md"

def _safe_title_from_record(record: Dict[str, Any]) -> str:
    return record.get("metadata", {}).get("title") or Path(record["path"]).stem

def _strip_frontmatter(text: str) -> str:
    t = text.lstrip()
    if not t.startswith("---"):
        return text
    lines = t.splitlines()
    # find second ---
    end_idx = None
    for i in range(1, min(len(lines), 200)):
        if lines[i].strip() == "---":
            end_idx = i
            break
    if end_idx is None:
        return text
    return "\n".join(lines[end_idx+1:]).lstrip()

def render_inline(record: Dict[str, Any]) -> RenderResult:
    """
    Decide HOW to render the item inline in the Streamlit app.
    This function is UI-aware (it calls small UI helper widgets)
    but the UI file itself doesn't branch on file types.
    """
    path = Path(record["path"])

    if not path.exists():
        # If the file is missing, at least show metadata
        return RenderResult(kind="metadata", metadata=record.get("metadata", {}), path=str(path))

    # PDF → inline PDF viewer
    if _is_pdf(path):
        render_pdf(path)
        return RenderResult(kind="inline_pdf", path=str(path), context={"title": _safe_title_from_record(record)})

    # Plain text or markdown → inline text/info viewer
    if _is_text(path):
        # You already have an "info" renderer. For .md you may later add a Markdown renderer.
        render_info(path)
        return RenderResult(kind="inline_text", path=str(path), context={"title": _safe_title_from_record(record)})
    
    
    if _is_markdown(path):
        st.subheader("📝 Markdown Preview")
        text = path.read_text(encoding="utf-8", errors="replace")
        # If you also want to hide front-matter from the preview:
        text = _strip_frontmatter(text)
        st.markdown(text)  # Streamlit supports standard Markdown
        return RenderResult(kind="inline_text", path=str(path))


    # Unknown binary types → show metadata only
    return RenderResult(kind="metadata", metadata=record.get("metadata", {}), path=str(path))

def export_document(record: Dict[str, Any], out_dir: Path) -> ExportResult:
    """
    Export the selected record to an output directory.
    For v1: we copy the source as-is for supported types; PDFs are directly downloadable.
    Later you can enhance this to transform MD->PDF, DOCX->PDF, etc.
    """
    path = Path(record["path"])
    out_dir.mkdir(parents=True, exist_ok=True)

    if not path.exists():
        return ExportResult(type="none", output=None, message=f"Source not found: {path}")

    ext = path.suffix.lower()

    # Simple pass-through export for supported types
    if ext in SUPPORTED_EXPORT:
        target = out_dir / path.name
        if target.resolve() == path.resolve():
            # Already in place
            return ExportResult(type="binary" if ext == ".pdf" else "text", output=str(target), message="Already exported.")
        shutil.copy2(path, target)
        return ExportResult(type="binary" if ext == ".pdf" else "text", output=str(target), message="Exported.")

    # Fallback: export metadata as JSON (optional future)
    # For now, just say not supported.
    return ExportResult(type="none", output=None, message=f"Export not supported for {ext}")