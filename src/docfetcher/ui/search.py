# src/docfetcher/ui/search.py
"""
 * Project:        KnowMore
 * File:           search.py
 * Description:    Search page UI for the KnowMore document fetcher application
 * Author:         Josh Cross
 * Created:        26/02/2026
 * Last Modified:  05/03/2026 by Josh Cross
 *
""" 

import streamlit as st
import docfetcher.state as state

def show_search_page(INDEX: list):
    st.markdown("""
    ## Search Your Documents 🔍

    Use the search bar below to find documents in your collection. You can filter by tags and sites to narrow down your results.
    """)
    
    
# Current site selection from global state (may be None if user chose "Search Documents")
    selected_site_state = state.get_selected_site()

    # Search input
    search_query = st.text_input("Search for documents...")

    # Extract unique tags and sites from the index
    all_tags = sorted({tag for r in INDEX for tag in r.get("metadata", {}).get("tags", [])})
    all_sites = sorted({r.get("metadata", {}).get("site") for r in INDEX if r.get("metadata", {}).get("site")})

    # Build site options and default index based on state
    site_options = ["(Any)"] + all_sites
    if selected_site_state in all_sites:
        default_site_index = site_options.index(selected_site_state)
    else:
        default_site_index = 0  # "(Any)"

    # Tag and site filters
    selected_tag = st.selectbox("Filter by Tag", ["(Any)"] + all_tags)
    selected_site = st.selectbox(
        "Filter by Site",
        site_options,
        index=default_site_index,
    )

    # Keep global state in sync with the user's site selection
    if selected_site == "(Any)":
        state.set_selected_site(None)
    else:
        state.set_selected_site(selected_site)

    def record_matches(r: dict) -> bool:
        meta = r.get("metadata", {})
        content = r.get("content", "") or ""

        if search_query and search_query.lower() not in content.lower():
            return False
        if selected_tag != "(Any)" and selected_tag not in meta.get("tags", []):
            return False
        if selected_site != "(Any)" and selected_site != meta.get("site"):
            return False
        return True

    filtered_records = [r for r in INDEX if record_matches(r)]

    st.markdown(f"### Found {len(filtered_records)} matching documents:")

    for i, doc in enumerate(filtered_records):
        meta = doc.get("metadata", {}) or {}
        title = meta.get("title", "Untitled Document")
        site = meta.get("site", "Unknown Site")
        tags = ", ".join(meta.get("tags", []))

        # Show some context in the UI
        st.write(f"**{title}**  \nSite: `{site}`  \nTags: {tags or '—'}")

        # Unique key per button to avoid Streamlit collisions
        if st.button(f"Preview: {title}", key=f"search_preview_{i}"):
            state.set_selected_doc_id(doc.get("id"))
            state.set_view("preview")

        st.markdown("---")
