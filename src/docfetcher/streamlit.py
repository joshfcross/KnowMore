# src/docfetcher/streamlit.py
"""
Project:        KnowMore
File:           streamlit.py
Description:    Streamlit UI for the KnowMore document fetcher application
Author:         Josh Cross
Created:        18/02/2026
Last Modified:  26/02/2026 by Josh Cross
"""

import streamlit as st
from pathlib import Path
import json

from docfetcher.renderer import render_inline, export_document

from docfetcher.state import get_view, set_view
from docfetcher.ui.landing import show_landing_page
from docfetcher.ui.search import show_search_page
from docfetcher.ui.site_select import show_site_select
from docfetcher.ui.site_browse import show_site_browse
from docfetcher.ui.preview import show_preview

view = get_view()

if view == "landing":
    show_landing_page()
elif view == "search":
    show_search_page()
elif view == "site_select":
    show_site_select()
elif view == "site_browse":
    show_site_browse()
elif view == "preview":
    show_preview()

ROOT = Path(__file__).resolve().parents[2]
INDEX = json.loads((ROOT / "data" / "index.json").read_text(encoding="utf-8"))

st.set_page_config(page_title="KnowMore", layout="wide")
st.title("📚 KnowMore - Document Fetcher")

# ---------------- Sidebar Filters ----------------
st.sidebar.header("Filters")

# Tag filter
all_tags = sorted({tag for r in INDEX for tag in r.get("metadata", {}).get("tags", [])})
selected_tag = st.sidebar.selectbox("Tags", ["(Any)"] + all_tags)

# Site filter (fixed)
all_sites = sorted({r.get("metadata", {}).get("site") for r in INDEX if r.get("metadata", {}).get("site")})
selected_site = st.sidebar.selectbox("Site", ["(Any)"] + all_sites)

def record_matches(r: dict) -> bool:
    meta = r.get("metadata", {})
    if selected_tag != "(Any)" and selected_tag not in meta.get("tags", []):
        return False
    if selected_site != "(Any)" and selected_site != meta.get("site"):
        return False
    return True

filtered_records = [r for r in INDEX if record_matches(r)]

# ---------------- Results ----------------
st.subheader("Matching Documents")

if not filtered_records:
    st.info("No documents match the selected filters.")
else:
    titles = [r.get("metadata", {}).get("title", Path(r["path"]).stem) for r in filtered_records]
    choice = st.selectbox("Select a document to view", ["(Select)"] + titles)

    if choice and choice != "(Select)":
        selected_record = filtered_records[titles.index(choice)]

        # Delegate inline rendering to the renderer (PDF, TXT, metadata)
        _ = render_inline(selected_record)  # UI shown by renderer

        # Export Button — also delegated
        if st.button("📄 Export Document"):
            out_dir = ROOT / "output" / "ui_export"
            result = export_document(selected_record, out_dir)
            if result.type == "none":
                st.warning(result.message or "Export failed.")
            else:
                st.success(result.message or "Exported!")
                st.write("Output file:", result.output)

                if result.type == "binary" and str(result.output).lower().endswith(".pdf"):
                    with open(result.output, "rb") as f:
                        st.download_button(
                            label="⬇️ Download PDF",
                            data=f,
                            file_name=Path(result.output).name,
                            mime="application/pdf",
                        )
    else:
        st.info("Select a document to view its details.")
