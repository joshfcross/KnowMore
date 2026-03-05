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
    
    # Guard against empty site
    if not selected_site:
        st.error("No site selected. Please go back and select a site to browse.")
        if st.button("Back to Site Selection"):
            state.set_view("site_select")
        return

    st.markdown(f"""
    ## Browsing Site: {selected_site} 🌐

    Here you can explore documents from the selected site. Use the filters in the sidebar to narrow down results.
    """)

    # Optional search within site only
    search_query = st.text_input(f"Search within {selected_site}...")

    def record_matches(r: dict) -> bool:
        meta = r.get("metadata", {})
        
        if meta.get("site") != selected_site:
            return False
        
        if search_query: 
            content = r.get("content", "") or ""
            if search_query.lower() not in content.lower():
                return False
        return True
    
    site_docs = [r for r in INDEX if record_matches(r)]

    
    st.markdown(f"### Found {len(site_docs)} documents in **{selected_site}**:")

    if not site_docs:
        st.info("No documents match your criteria for this site.")
    else:
        for i, doc in enumerate(site_docs):
            meta = doc.get("metadata", {}) or {}
            title = meta.get("title", "Untitled Document")
            tags = ", ".join(meta.get("tags", []))

            st.write(f"**{title}**  \nTags: {tags or '—'}")

            if st.button(f"Preview: {title}", key=f"site_browse_preview_{i}"):
                state.set_selected_doc_id(doc.get("id"))
                state.set_view("preview")

            st.markdown("---")

    # Navigation back
    if st.button("Back to Site Selection"):
        state.set_view("site_select")