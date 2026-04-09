# src/docfetcher/ui/preview.py
"""
 * Project:        KnowMore
 * File:           preview.py
 * Description:    Preview UI for the KnowMore document fetcher application
 * Author:         Josh Cross
 * Created:        26/02/2026
 * Last Modified:  26/02/2026 by Josh Cross
 *
""" 

import streamlit as st
import docfetcher.state as state

def show_preview(INDEX: list):
    selected_doc_id = state.get_selected_doc_id()
    if not selected_doc_id:
        st.error("No document selected for preview.")
        return
    
    # Find the document in the index
    doc = next((r for r in INDEX if r.get("id") == selected_doc_id), None)
    
    if not doc:
        st.error("Selected document not found in index.")
        return
    
    st.markdown(f"## Preview: {doc.get('metadata', {}).get('title', 'Untitled Document')}")
    st.markdown(f"**Site:** {doc.get('metadata', {}).get('site', 'Unknown')}")
    st.markdown(f"**Tags:** {', '.join(doc.get('metadata', {}).get('tags', []))}")
    
    content = doc.get("content", "No content available for preview.")
    st.text_area("Document Content", value=content, height=300)