import os
import json
from docx import Document
from pathlib import Path

def get_row_text(row):
    texts = []
    seen = set()
    for cell in row.cells:
        t = cell.text.strip()
        if t and t not in seen:
            texts.append(t)
            seen.add(t)
    return " | ".join(texts)

def extract_grid(table):
    grid_data = {}
    if len(table.rows) >= 8:
        grid_data["demographics_row"] = get_row_text(table.rows[1])
        grid_data["pathology_row"] = get_row_text(table.rows[3])
        grid_data["endoscopy_row"] = get_row_text(table.rows[5])
        grid_data["outcome_row"] = get_row_text(table.rows[7])
    return grid_data

def main():
    print("Grid Extractor restored for v3.")

if __name__ == "__main__":
    main()
