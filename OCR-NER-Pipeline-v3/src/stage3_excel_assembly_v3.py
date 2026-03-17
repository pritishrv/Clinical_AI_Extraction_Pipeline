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
INPUT_DIR = PROJECT_ROOT / "OCR-NER-Pipeline-v3/output/json_ner"
PROTOTYPE_WORKBOOK = PROJECT_ROOT / "data/hackathon-database-prototype.xlsx"
OUTPUT_WORKBOOK = PROJECT_ROOT / "OCR-NER-Pipeline-v3/output/generated-database-v3.xlsx"

def clean_date(text):
    if not text: return ""
    match = re.search(r"(\d{1,2}[/\-\.]\d{1,2}[/\-\.]\d{2,4})", text)
    if not match: return ""
    val = match.group(1).replace("-", "/").replace(".", "/")
    parts = val.split("/")
    if len(parts) == 3:
        day, month, year = parts
        if len(year) == 2: year = f"20{year}"
        return f"{day.zfill(2)}/{month.zfill(2)}/{year}"
    return val

def extract_initials(text):
    match = re.search(r"Name:\s*([^|]+)", text, re.I)
    if not match: return ""
    name = match.group(1).strip()
    parts = [p for p in name.split() if p]
    if not parts: return ""
    if len(parts) == 1: return parts[0][0].upper()
    return f"{parts[0][0].upper()}{parts[-1][0].upper()}"

def classify_treatment(text):
    lowered = text.lower()
    if "foxtrot" in lowered: return "downstaging chemotherapy"
    if any(x in lowered for x in ["crt", "chemoradiotherapy"]): return "downstaging nCRT"
    if "watch and wait" in lowered: return "Papillon +/- EBRT"
    if any(x in lowered for x in ["surgery", "hemicolectomy", "resection"]): return "straight to surgery"
    return ""

def map_ner_to_row(case_data):
    entities = case_data["entities"]
    rows = case_data["rows"]
    full_text = " | ".join([r["text"] for r in rows])
    
    def get_ent(label, negated=None):
        for ent in entities:
            if ent["label"] == label:
                if negated is None or ent["negated"] == negated:
                    return ent["text"]
        return ""

    # Improved regex for identifiers that might miss the NER matcher
    nhs_match = re.search(r"NHS\s*Number\s*[:\-\u2013]?\s*(\d+)", full_text, re.I)
    mrn_match = re.search(r"Hospital\s*Number\s*[:\-\u2013]?\s*(\d+)", full_text, re.I)
    dob_match = re.search(r"DOB\s*[:\-\u2013]?\s*(\d{1,2}[/\-\.]\d{1,2}[/\-\.]\d{2,4})", full_text, re.I)

    row_data = {
        "Demographics: \nDOB(a)": clean_date(dob_match.group(1) if dob_match else get_ent("DOB")),
        "Demographics: Initials(b)": extract_initials(full_text),
        "Demographics: MRN(c)": mrn_match.group(1) if mrn_match else re.sub(r"\D", "", get_ent("MRN")),
        "Demographics: \nNHS number(d)": nhs_match.group(1) if nhs_match else re.sub(r"\D", "", get_ent("NHS_NUMBER")),
        "Demographics: \nGender(e)": "Male" if "Male" in full_text else "Female" if "Female" in full_text else "",
        "Demographics:\nPrevious cancer \n(y, n) \nif yes, where(f)": "Yes" if "previous cancer" in full_text.lower() else "No",
        "Demographics: \nState site of previous cancer(f)": "N/A" if "previous cancer" not in full_text.lower() else "",
    }

    # Histology
    row_data["Histology: Biopsy result(g)"] = ""
    for r in rows:
        if "Diagnosis:" in r["text"]:
            row_data["Histology: Biopsy result(g)"] = r["text"].split("Diagnosis:")[1].split("|")[0].strip()
            break
    row_data["Histology: \nMMR status(g/h)"] = "Deficient" if "MMR deficient" in full_text else "Proficient" if "MMR proficient" in full_text else ""

    # Endoscopy
    row_data["Endoscopy: date(f)"] = ""
    row_data["Endosopy type: flexi sig, incomplete colonoscopy, colonoscopy complete - if gets to ileocecal valve(f) "] = ""
    row_data["Endoscopy: Findings(f)"] = ""
    for r in rows:
        if any(p in r["text"].lower() for p in ["colonoscopy", "flexi sig", "sigmoidoscopy"]):
            row_data["Endosopy type: flexi sig, incomplete colonoscopy, colonoscopy complete - if gets to ileocecal valve(f) "] = r["text"].split("|")[0].strip()
            row_data["Endoscopy: Findings(f)"] = r["text"]
            date_match = re.search(r"(\d{1,2}[/\-\.]\d{1,2}[/\-\.]\d{2,4})", r["text"])
            if date_match: row_data["Endoscopy: date(f)"] = clean_date(date_match.group(1))
            break

    # Staging - CT
    row_data["Baseline CT: Date(h)"] = ""
    ct_found = False
    for r in rows:
        if "CT" in r["text"]:
            row_data["Baseline CT: Date(h)"] = clean_date(r["text"])
            ct_found = True
            break
    
    row_data["Baseline CT: T(h)"] = get_ent("T_STAGE")
    row_data["Baseline CT: N(h)"] = get_ent("N_STAGE")
    row_data["Baseline CT: M(h)"] = "1" if "metastases" in full_text.lower() and "no metastases" not in full_text.lower() else "0"
    row_data["Baseline CT: EMVI(h)"] = get_ent("EMVI")
    
    # Staging - MRI
    row_data["Baseline MRI: date(h)"] = ""
    for r in rows:
        if "MRI" in r["text"] or "MR " in r["text"]:
            row_data["Baseline MRI: date(h)"] = clean_date(r["text"])
            break
            
    row_data["Baseline MRI: mrT(h)"] = get_ent("T_STAGE")
    row_data["Baseline MRI: mrN(h)"] = get_ent("N_STAGE")
    row_data["Baseline MRI: mrEMVI(h)"] = get_ent("EMVI")
    row_data["Baseline MRI: mrCRM(h)"] = get_ent("CRM")
    row_data["Baseline MRI: mrPSW(h)"] = get_ent("PSW")

    # MDT Date
    row_data["1st MDT: date(i)"] = ""
    mdt_date_match = re.search(r"(\d{2}/\d{2}/\d{4})\(i\)", full_text)
    if mdt_date_match:
        row_data["1st MDT: date(i)"] = mdt_date_match.group(1)

    # MDT Decision & Treatment
    row_data["1st MDT: Treatment approach \n(TNT, downstaging chemotherapy, downstaging nCRT, downstaging shortcourse RT, Papillon +/- EBRT, straight to surgery(h)"] = classify_treatment(full_text)
    row_data["MDT (after 6 week: Decision "] = ""
    for r in rows:
        if "Outcome:" in r["text"]:
            row_data["MDT (after 6 week: Decision "] = r["text"].split("Outcome:")[1].strip()
            break

    return row_data

def main():
    if not os.path.exists(OUTPUT_WORKBOOK.parent): os.makedirs(OUTPUT_WORKBOOK.parent)
    ner_files = sorted([f for f in os.listdir(INPUT_DIR) if f.endswith(".json")])
    all_rows = [map_ner_to_row(json.load(open(INPUT_DIR / f))) for f in ner_files]
    df = pd.DataFrame(all_rows)
    template_cols = list(pd.read_excel(PROTOTYPE_WORKBOOK).columns)
    df = df.reindex(columns=template_cols).fillna("")
    write_styled_workbook(df, PROTOTYPE_WORKBOOK, OUTPUT_WORKBOOK)
    print(f"Generated v3 database saved to {OUTPUT_WORKBOOK}")

if __name__ == "__main__":
    main()
