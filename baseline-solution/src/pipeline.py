import re
from pathlib import Path

import pandas as pd

from extract_fields import extract_case_fields
from load_docx import load_cases
from write_excel import write_styled_workbook


ROOT_DIR = Path(__file__).resolve().parents[2]
BASELINE_SOLUTION_DIR = ROOT_DIR / "baseline-solution"
OUTPUT_WORKBOOK = BASELINE_SOLUTION_DIR / "output" / "generated-database-gemini.xlsx"
DOCX_INPUT = ROOT_DIR / "data" / "hackathon-mdt-outcome-proformas.docx"
PROTOTYPE_WORKBOOK = ROOT_DIR / "data" / "hackathon-database-prototype.xlsx"

def main():
    # Load Cases
    cases, doc = load_cases(str(DOCX_INPUT))
    print(f"Loaded {len(cases)} cases.")

    # Extract common MDT Date from document title
    # e.g., Colorectal Multidisciplinary Meeting 07/03/2025(i)
    doc_date = None
    for para in doc.paragraphs:
        if "Multidisciplinary Meeting" in para.text:
            date_match = re.search(r'(\d{2}/\d{2}/\d{4})\(i\)', para.text)
            if date_match:
                doc_date = date_match.group(1)
                print(f"Found MDT Date: {doc_date}")
                break

    # Extract fields for each case
    extracted_data = []
    for case in cases:
        fields = extract_case_fields(case, doc_date=doc_date)
        extracted_data.append(fields)

    # Convert to DataFrame
    df = pd.DataFrame(extracted_data)

    # Normalize: Patient identity resolution (not strictly needed for this synthetic set as 1 case per table, but let's see if repeated discussions)
    # The requirement says "preserve repeated patient discussions as sequential longitudinal events".
    # In this dataset, there are 50 cases. If NHS Number repeats, they should be rows.
    # The DataFrame already holds one row per discussion.
    
    # Sort by NHS Number and Date to ensure longitudinal order
    if 'Demographics: \nNHS number(d)' in df.columns and '1st MDT: date(i)' in df.columns:
        df = df.sort_values(by=['Demographics: \nNHS number(d)', '1st MDT: date(i)'])

    # Get prototype columns for alignment
    template_cols = list(pd.read_excel(PROTOTYPE_WORKBOOK, sheet_name=0).columns)
    
    # Reindex DataFrame to match template columns
    df_aligned = df.reindex(columns=template_cols)

    # Write to Excel using the prototype workbook's styling.
    write_styled_workbook(df_aligned, PROTOTYPE_WORKBOOK, OUTPUT_WORKBOOK)
    print(f"Generated workbook saved to {OUTPUT_WORKBOOK}")

if __name__ == "__main__":
    main()
