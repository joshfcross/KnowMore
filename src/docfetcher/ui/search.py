# src/docfetcher/ui/search.py
"""
 * Project:        KnowMore
 * File:           search.py
 * Description:    Search page UI for the KnowMore document fetcher application
 * Author:         Josh Cross
 * Created:        26/02/2026
 * Last Modified:  26/02/2026 by Josh Cross
 *
""" 

import streamlit as st
import docfetcher.state as state

def show_search_page(INDEX: list):
    st.markdown("""
    ## Search Your Documents 🔍

    Use the search bar below to find documents in your collection. You can filter by tags and sites to narrow down your results.
    """)
    
    # Search input
    search_query = st.text_input("Search for documents...")
    
    # Extract unique tags and sites from the index
    all_tags = sorted({tag for r in INDEX for tag in r.get("metadata", {}).get("tags", [])})
    all_sites = sorted({r.get("metadata", {}).get("site") for r in INDEX if r.get("metadata", {}).get("site")})
    
    # Tag and site filters
    selected_tag = st.selectbox("Filter by Tag", ["(Any)"] + all_tags)
    selected_site = st.selectbox("Filter by Site", ["(Any)"] + all_sites)
    
    def record_matches(r: dict) -> bool:
        meta = r.get("metadata", {})
        if search_query and search_query.lower() not in r.get("content", "").lower():
            return False
        if selected_tag != "(Any)" and selected_tag not in meta.get("tags", []):
            return False
        if selected_site != "(Any)" and selected_site != meta.get("site"):
            return False
        return True
    
    filtered_records = [r for r in INDEX if record_matches(r)]
    
    st.markdown(f"### Found {len(filtered_records)} matching documents:")
    
    for doc in filtered_records:
        title = doc.get("metadata", {}).get("title", "Untitled Document")
        site = doc.get("metadata", {}).get("site", "Unknown Site")
        tags = ", ".join(doc.get("metadata", {}).get("tags", []))
        
        if st.button(f"Preview: {title} ({site})"):
            state.set_selected_doc_id(doc.get("id"))
            state.set_view("preview")