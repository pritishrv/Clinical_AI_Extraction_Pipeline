import re
from pathlib import Path

import pandas as pd

from codex_extract_fields import extract_case_fields_codex
from load_docx import load_cases
from write_excel import write_styled_workbook


ROOT_DIR = Path(__file__).resolve().parents[2]
BASELINE_SOLUTION_DIR = ROOT_DIR / "baseline-solution"
OUTPUT_WORKBOOK = BASELINE_SOLUTION_DIR / "output" / "generated-database-codex.xlsx"
DOCX_INPUT = ROOT_DIR / "data" / "hackathon-mdt-outcome-proformas.docx"
PROTOTYPE_WORKBOOK = ROOT_DIR / "data" / "hackathon-database-prototype.xlsx"


def _extract_document_mdt_date(doc):
    for paragraph in doc.paragraphs:
        if "Multidisciplinary Meeting" in paragraph.text:
            match = re.search(r"(\d{2}/\d{2}/\d{4})\(i\)", paragraph.text)
            if match:
                return match.group(1)
    return ""


def main():
    cases, doc = load_cases(str(DOCX_INPUT))
    print(f"Loaded {len(cases)} cases.")

    doc_date = _extract_document_mdt_date(doc)
    if doc_date:
        print(f"Found MDT Date: {doc_date}")

    extracted_data = [extract_case_fields_codex(case, doc_date=doc_date) for case in cases]
    dataframe = pd.DataFrame(extracted_data)

    template_columns = list(pd.read_excel(PROTOTYPE_WORKBOOK, sheet_name=0).columns)
    dataframe = dataframe.reindex(columns=template_columns)

    if "Demographics: \nNHS number(d)" in dataframe.columns and "1st MDT: date(i)" in dataframe.columns:
        dataframe = dataframe.sort_values(
            by=["Demographics: \nNHS number(d)", "1st MDT: date(i)"],
            na_position="last",
        ).reset_index(drop=True)

    write_styled_workbook(dataframe, PROTOTYPE_WORKBOOK, OUTPUT_WORKBOOK)
    print(f"Generated workbook saved to {OUTPUT_WORKBOOK}")


if __name__ == "__main__":
    main()
