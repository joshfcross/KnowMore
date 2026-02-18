"""
 * Project:        KnowMore
 * File:           test_run.py
 * Description:    Test runner for the KnowMore document fetcher application
 * Author:         Josh Cross
 * Created:        18/02/2026
 * Last Modified:  18/02/2026 by Josh Cross
 *
""" 

# Public modules
from pathlib import Path
import json

# Repository modules
from docfetcher.renderer import render_document

index_path = Path(__file__).resolve().parents[2] / "data" / "index.json"
index = json.loads(index_path.read_text())

# Pick the first binary doc you have
record = next(r for r in index if r["type"] == "binary")

print("Found:", record["metadata"].get("title"))

output = render_document(record, Path("output/test"))
print("Output:", output)