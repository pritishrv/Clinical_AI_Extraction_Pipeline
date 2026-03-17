import os
import json
import pandas as pd
import re
from pathlib import Path
from sys import path

# Add the baseline-solution/src to path to import write_styled_workbook
PROJECT_ROOT = Path("/Users/joshuabhawanlall/Git Folder/Clinical_AI_Extraction_Pipeline")
path.append(str(PROJECT_ROOT / "baseline-solution/src"))

from write_excel import write_styled_workbook

# Configuration
INPUT_DIR = PROJECT_ROOT / "OCR-NER-Pipeline-v3/output/json_ner_v4"
PROTOTYPE_WORKBOOK = PROJECT_ROOT / "data/hackathon-database-prototype.xlsx"
OUTPUT_WORKBOOK = PROJECT_ROOT / "OCR-NER-Pipeline-v3/output/generated-database-v4.xlsx"

def clean_date(text):
    if not text: return ""
    match = re.search(r"(\d{1,2}[/\-\.]\d{1,2}[/\-\.]\d{2,4})", text)
    if not match: return ""
    val = match.group(1).replace("-", "/").replace(".", "/")
    parts = val.split("/")
    if len(parts) == 3:
        d, m, y = parts
        if len(y) == 2: y = f"20{y}"
        return f"{d.zfill(2)}/{m.zfill(2)}/{y}"
    return val

def map_ner_to_row(case_data):
    entities = case_data["entities"]
    full_text = case_data["full_text"]
    
    def get_ent(label, negated=None):
        for ent in entities:
            if ent["label"] == label:
                if negated is None or ent["negated"] == negated:
                    return ent["text"]
        return ""

    # Identifiers
    nhs_match = re.search(r"NHS\s*Number\s*[:\-\u2013]?\s*(\d+)", full_text, re.I)
    mrn_match = re.search(r"Hospital\s*Number\s*[:\-\u2013]?\s*(\d+)", full_text, re.I)
    dob_match = re.search(r"DOB\s*[:\-\u2013]?\s*(\d{1,2}[/\-\.]\d{1,2}[/\-\.]\d{2,4})", full_text, re.I)

    row_data = {
        "Demographics: \nDOB(a)": clean_date(dob_match.group(1) if dob_match else get_ent("DOB")),
        "Demographics: MRN(c)": mrn_match.group(1) if mrn_match else re.sub(r"\D", "", get_ent("MRN")),
        "Demographics: \nNHS number(d)": nhs_match.group(1) if nhs_match else re.sub(r"\D", "", get_ent("NHS_NUMBER")),
        "Demographics: \nGender(e)": "Male" if "Male" in full_text else "Female" if "Female" in full_text else "",
    }

    # MDT Date (often in the paragraph header)
    mdt_date_match = re.search(r"MDT\s+Date\s*[:\-\u2013]?\s*(\d{1,2}[/\-\.]\d{1,2}[/\-\.]\d{2,4})", full_text, re.I)
    if mdt_date_match:
        row_data["1st MDT: date(i)"] = clean_date(mdt_date_match.group(1))

    # Histology
    row_data["Histology: \nMMR status(g/h)"] = "Deficient" if "MMR deficient" in full_text else "Proficient" if "MMR proficient" in full_text else ""
    if "Diagnosis:" in full_text:
        row_data["Histology: Biopsy result(g)"] = full_text.split("Diagnosis:")[1].split("|")[0].strip()

    # Staging
    row_data["Baseline CT: T(h)"] = get_ent("T_STAGE")
    row_data["Baseline CT: N(h)"] = get_ent("N_STAGE")
    row_data["Baseline CT: M(h)"] = "1" if "metastases" in full_text.lower() and "no metastases" not in full_text.lower() else "0"
    
    row_data["Baseline MRI: mrT(h)"] = get_ent("MR_T_STAGE") or get_ent("T_STAGE")
    row_data["Baseline MRI: mrN(h)"] = get_ent("MR_N_STAGE") or get_ent("N_STAGE")
    row_data["Baseline MRI: mrEMVI(h)"] = get_ent("EMVI")
    row_data["Baseline MRI: mrCRM(h)"] = get_ent("CRM")

    return row_data

def main():
    if not os.path.exists(OUTPUT_WORKBOOK.parent): os.makedirs(OUTPUT_WORKBOOK.parent)
    ner_files = sorted([f for f in os.listdir(INPUT_DIR) if f.endswith(".json")])
    all_rows = [map_ner_to_row(json.load(open(INPUT_DIR / f))) for f in ner_files]
    df = pd.DataFrame(all_rows)
    template_cols = list(pd.read_excel(PROTOTYPE_WORKBOOK).columns)
    df = df.reindex(columns=template_cols).fillna("")
    write_styled_workbook(df, PROTOTYPE_WORKBOOK, OUTPUT_WORKBOOK)
    print(f"Generated v4 database saved to {OUTPUT_WORKBOOK}")

if __name__ == "__main__":
    main()
