# src/docfetcher/ui_state.py
"""
Project:        KnowMore
File:           ui_state.py
Description:    Streamlit UI state management for the KnowMore document fetcher application
Author:         Josh Cross
Created:        26/02/2026
Last Modified:  26/02/2026 by Josh Cross
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