# src/docfetcher/ui/site_browse.py
"""
 * Project:        KnowMore
 * File:           site_browse.py
 * Description:    Site browsing UI for the KnowMore document fetcher application
 * Author:         Josh Cross
 * Created:        26/02/2026
 * Last Modified:  26/02/2026 by Josh Cross
 *
""" 

import streamlit as st
import docfetcher.state as state

def show_site_browse(INDEX: list):
    selected_site = state.get_selected_site()
    
    st.markdown(f"""
    ## Browsing Site: {selected_site} 🌐

    Here you can explore documents from the selected site. Use the filters in the sidebar to narrow down results.
    """)