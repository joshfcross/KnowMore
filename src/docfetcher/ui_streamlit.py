import streamlit as st
from pathlib import Path
import json

from docfetcher.renderer import render_document

ROOT = Path(__file__).resolve().parents[2]
INDEX_PATH = json.loads((ROOT / "data" / "index.json").read_text())

st.set_page_config(page_title="KnowMore", layout="wide")
st.title("📚 KnowMore - Document Fetcher")

"""   Sidebar: Filters  """

st.sidebar.header("Filters")

# Tag filter
all_tags = sorted({tag for r in INDEX_PATH for tag in r["metadata"].get("tags", [])  })
selected_tags = st.sidebar.selectbox("Tags", ["(Any)"] + all_tags)

# Site filter
all_sites = sorted({r["metadata"].get("site") for r in INDEX_PATH if "site" in r["metadata"].get("site",)})
selected_site = st.sidebar.selectbox("Site", ["(Any)"] + all_sites)

"""   Filter: Records   """

def record_matches(record):
    if selected_tags != "(Any)" and selected_tags not in record["metadata"].get("tags", []):
        return False  
    if selected_site != "(Any)" and selected_site != record["metadata"].get("site"):
        return False
    return True

filtered_records = [r for r in INDEX_PATH if record_matches(r)]

"""   Display: Results   """

st.subheader("Matching Documents")

if not filtered_records:
    st.info("No documents match the selected filters.")
else:
    titles = [r["metadata"].get("title", Path(r["path"]).stem) for r in filtered_records]
    choice = st.selectbox("Select a document to view", ["(Select)"] + titles)

    if choice and choice != "(Select)":
        selected_record = filtered_records[titles.index(choice)]

        st.write("*Metadata:*")
        st.json(selected_record["metadata"])

        # Render Button

        if st.button("📄 Export Document"):
            out_dir = ROOT / "output" / "ui_export"
            result = render_document(selected_record, out_dir)
            st.success("Exported!")
            st.write("Output file:", result["output"])

            if result["type"] == "binary" and result["output"].endswith(".pdf"):
                with open(result["output"], "rb") as f:
                    st.download_button(
                        label="⬇️ Download PDF",
                        data=f,
                        file_name=Path(result["output"]).name,
                        mime="application/pdf",
                    )
    else:
        st.info("Select a document to view its details.")
