"""
 * Project:        KnowMore
 * File:           ui_helpers.py
 * Description:    Streamlit UI helper functions for the KnowMore document fetcher application
 * Author:         Josh Cross
 * Created:        18/02/2026
 * Last Modified:  18/02/2026 by Josh Cross
 *
""" 

# Public modules
import streamlit as st
from streamlit_pdf_viewer import pdf_viewer
from pathlib import Path

"""   Render: PDF   """

def render_pdf(path: str | Path):
    path = Path(path)

    if not path.exists():
        st.error(f"PDF not found: {path}")
        return
    
    st.subheader("📄 PDF Preview")
    
    with open(path, "rb") as f:
        pdf_data = f.read()
    pdf_viewer(pdf_data, width=800, height=900)