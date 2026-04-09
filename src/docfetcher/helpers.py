# src/docfetcher/helpers.py
"""
Project:        KnowMore
File:           helpers.py
Description:    Streamlit UI helper functions for the KnowMore document fetcher application
Author:         Josh Cross
Created:        18/02/2026
Last Modified:  26/02/2026 by Josh Cross
"""

import streamlit as st
from streamlit_pdf_viewer import pdf_viewer
from pathlib import Path

# Render PDF documents
def render_pdf(path: str | Path):
    path = Path(path)
    if not path.exists():
        st.error(f"PDF not found: {path}")
        return
    st.subheader("📄 PDF Preview")
    with open(path, "rb") as f:
        pdf_data = f.read()
    pdf_viewer(pdf_data, width=800, height=900)

# Render information documents
def render_info(path: str | Path):
    path = Path(path)
    if not path.exists():
        st.error(f"File not found: {path}")
        return

    st.subheader("ℹ️ Document Info")
    st.write(f"**Path:** {path}")
    st.write(f"**Size:** {path.stat().st_size / 1024:.2f} KB")

    # If it's a text file, show contents
    if path.suffix.lower() in {".txt", ".md"}:
        st.subheader("📄 Contents")
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except Exception as e:
            st.warning(f"Could not read text: {e}")
            return
        # For .md you might later use st.markdown(text, unsafe_allow_html=False)
        st.code(text)

# ender metadata dictionary in a nice format
def render_metadata(metadata: dict):
    st.subheader("🗂️ Metadata")
    for key, value in metadata.items():
        st.write(f"**{key.capitalize()}:** {value}")

# Render Markdown documents (simple rendering for now)
def render_markdown(path: str | Path):
    path = Path(path)
    if not path.exists():
        st.error(f"Markdown file not found: {path}")
        return
    st.subheader("📄 Markdown Preview")
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        st.warning(f"Could not read markdown: {e}")
        return
    st.markdown(text, unsafe_allow_html=False)