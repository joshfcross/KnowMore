# src/docfetcher/state.py
"""
Project:        KnowMore
File:           state.py
Description:    Streamlit UI state management for the KnowMore document fetcher application
Author:         Josh Cross
Created:        26/02/2026
Last Modified:  05/03/2026 by Josh Cross
"""
import streamlit as st

VALID_VIEWS = {"landing", "search", "site_select", "site_browse", "preview"}

def get_view():
    return st.session_state.get("view", "landing")

def set_view(view: str):
    if view in VALID_VIEWS:
        st.session_state["view"] = view
    else:
        raise ValueError(f"Invalid view: {view}")

# --- Site selection state ---
def get_selected_site() -> str | None:
    return st.session_state.get("selected_site")

def set_selected_site(site: str | None):
    st.session_state["selected_site"] = site

# --- Document selection state ---
def get_selected_doc_id() -> str | None:
    return st.session_state.get("selected_doc_id")

def set_selected_doc_id(doc_id: str | None):
    st.session_state["selected_doc_id"] = doc_id