# src/docfetcher/ui/landing.py
"""
 * Project:        KnowMore
 * File:           landing.py
 * Description:    Landing page UI for the KnowMore document fetcher application
 * Author:         Josh Cross
 * Created:        26/02/2026
 * Last Modified:  05/03/2026 by Josh Cross
 *
"""

import streamlit as st
import docfetcher.state as state

st.title("📚 KnowMore - Document Fetcher")

def show_landing_page():
    st.markdown("""
    ## Welcome to KnowMore! 📚

    Your all-in-one document fetcher and knowledge management tool. 

    **Features:**
    - Fetch documents from various sources with ease
    - Organize and tag your documents for easy retrieval
    - Search through your collection with powerful filters
    - Preview document content before opening

    **Get Started:**
    Click the button below to start fetching documents and building your knowledge base!
    """)
    
    if st.button("Search Documents"):
        state.set_selected_site(None)  # Clear any previously selected site
        state.set_view("search")
    elif st.button("Select Sites"):
        state.set_view("site_select")
    
    st.markdown("""
    **Need Help?**
    - Check out our [documentation](https://knowmore-docs.example.com) for detailed guides and FAQs.
    - Contact our support team
    """)