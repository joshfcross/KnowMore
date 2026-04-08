# src/docfetcher/streamlit.py
"""
Project:        KnowMore
File:           streamlit.py
Description:    Streamlit UI for the KnowMore document fetcher application
Author:         Josh Cross
Created:        18/02/2026
Last Modified:  05/03/2026 by Josh Cross
"""

#Public Libraries
import streamlit as st
from pathlib import Path
import json
# Helpers
from docfetcher.renderer import render_inline, export_document
# States
from docfetcher.state import get_view, set_view
from docfetcher.ui.landing import show_landing_page
from docfetcher.ui.search import show_search_page
from docfetcher.ui.site_select import show_site_select
from docfetcher.ui.site_browse import show_site_browse
from docfetcher.ui.preview import show_preview

# ---------------- Main App ----------------
# Set Streamlit page configuration
st.set_page_config(page_title="KnowMore", layout="wide")

@st.cache_data
def load_index():
    return json.loads(((Path(__file__).resolve().parents[2]) / "data" / "index.json").read_text(encoding="utf-8"))

INDEX = load_index()

# Initialize view state if not set
if "view" not in st.session_state:
    set_view("landing")

# Determine which view to show based on the current state
view = get_view()

match view:
    case "landing":
        show_landing_page()
    case "search":
        show_search_page(INDEX)
    case "site_select":
        show_site_select(INDEX)
    case "site_browse":
        show_site_browse(INDEX)
    case "preview":
        show_preview(INDEX)
    case _:
        st.error(f"Unknown view: {view}")
