# src/docfetcher/ui/site_select.py
"""
 * Project:        KnowMore
 * File:           site_select.py
 * Description:    Site selection UI for the KnowMore document fetcher application
 * Author:         Josh Cross
 * Created:        26/02/2026
 * Last Modified:  26/02/2026 by Josh Cross
 *
""" 

import streamlit as st
import docfetcher.state as state

def show_site_select(INDEX: list):
    st.markdown("""
    ## Select a Site to Browse 🌐

    Choose from the list of sites available in your document index to explore and fetch documents.
    """)
    
    # Extract unique sites from the index
    all_sites = sorted({r.get("metadata", {}).get("site") for r in INDEX if r.get("metadata", {}).get("site")})
    
    selected_site = st.selectbox("Available Sites", ["(Select a site)"] + all_sites)
    
    if selected_site != "(Select a site)":
        state.set_view("site_browse")
        state.set_selected_site(selected_site)