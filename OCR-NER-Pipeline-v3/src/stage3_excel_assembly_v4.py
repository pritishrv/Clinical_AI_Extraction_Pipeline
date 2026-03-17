import os
import json
import pandas as pd
import re
from pathlib import Path
from sys import path
from copy import copy
from openpyxl import load_workbook

# Configuration
PROJECT_ROOT = Path("/Users/joshuabhawanlall/Git Folder/Clinical_AI_Extraction_Pipeline")
INPUT_DIR = PROJECT_ROOT / "OCR-NER-Pipeline-v3/output/json_ner_v4"
PROTOTYPE_WORKBOOK = PROJECT_ROOT / "data/hackathon-database-prototype.xlsx"
OUTPUT_WORKBOOK = PROJECT_ROOT / "OCR-NER-Pipeline-v3/output/generated-database-v4.xlsx"

def clean_date(text):
    if not text: return ""
    match = re.search(r"(\d{1,2})[/\-\.](\d{1,2})[/\-\.](\d{2,4})", text)
    if not match: return ""
    d, m, y = match.groups()
    if len(y) == 2: y = f"19{y}" if int(y) > 30 else f"20{y}"
    return f"{d.zfill(2)}/{m.zfill(2)}/{y}"

def map_ner_to_row(case_data):
    full_text = case_data["full_text"]
    parts = full_text.split("||")
    table_content = parts[0]
    entities = case_data["entities"]
    
    row_data = {}
    
    # 1. Demographics
    mrn_match = re.search(r"Hospital Number:\s*(\d+)", table_content, re.I)
    if mrn_match: row_data["Demographics: MRN(c)"] = mrn_match.group(1)
    
    nhs_match = re.search(r"NHS Number:\s*(\d+)", table_content, re.I)
    if nhs_match: row_data["Demographics: \nNHS number(d)"] = nhs_match.group(1)
    
    # Initials: Refined to handle apostrophes (O'Connor -> AO)
    lines = [l.strip() for l in table_content.split("|") if l.strip()]
    for i, line in enumerate(lines):
        if "(b)" in line:
            name = line.replace("(b)", "").strip()
            if not name and i > 0: name = lines[i-1].strip()
            if name and name.isupper():
                # Split only on spaces to preserve surnames like O'Connor
                parts = [p for p in name.split() if p]
                if len(parts) >= 2:
                    row_data["Demographics: Initials(b)"] = f"{parts[0][0].upper()}{parts[-1][0].upper()}"
                elif len(parts) == 1:
                    row_data["Demographics: Initials(b)"] = parts[0][0].upper()
                break

    dob_match = re.search(r"(\d{1,2}/\d{1,2}/\d{4})\(a\)", table_content)
    if dob_match: row_data["Demographics: \nDOB(a)"] = dob_match.group(1)

    if "Male(e)" in table_content: row_data["Demographics: \nGender(e)"] = "Male"
    elif "Female(e)" in table_content: row_data["Demographics: \nGender(e)"] = "Female"

    # 2. Histology & Site
    if "Diagnosis:" in table_content:
        diag_part = table_content.split("Diagnosis:")[1].split("|")[0].strip()
        row_data["Histology: Biopsy result(g)"] = diag_part.replace("\n", " ")
        if "rectum" in diag_part.lower(): row_data["Demographics: \nState site of previous cancer(f)"] = "Rectum"
        elif "colon" in diag_part.lower(): row_data["Demographics: \nState site of previous cancer(f)"] = "Colon"

    row_data["Histology: \nMMR status(g/h)"] = "Deficient" if "MMR deficient" in full_text else "Proficient" if "MMR proficient" in full_text else ""

    # 3. Endoscopy
    endo_match = re.search(r"(Colonoscopy|Flexi sig|Sigmoidoscopy)\s*:(.*?)(?:Discuss|MDT|CT|MRI|\|)", table_content, re.S | re.I)
    if endo_match:
        row_data["Endosopy type: flexi sig, incomplete colonoscopy, colonoscopy complete - if gets to ileocecal valve(f) "] = endo_match.group(1).strip()
        row_data["Endoscopy: Findings(f)"] = endo_match.group(2).strip().replace("\n", " ")

    # 4. CT Staging
    ct_match = re.search(r"CT\s+(\d{1,2}/\d{1,2}/\d{4}):(.*?)(?:MRI|Colonoscopy|\|)", table_content, re.S | re.I)
    if ct_match:
        row_data["Baseline CT: Date(h)"] = ct_match.group(1)
        ct_findings = ct_match.group(2).lower()
        t_val = re.search(r"\bT(\d[a-d]?)\b", ct_findings)
        n_val = re.search(r"\bN(\d[a-c]?)\b", ct_findings)
        if t_val: row_data["Baseline CT: T(h)"] = t_val.group(1)
        if n_val: row_data["Baseline CT: N(h)"] = n_val.group(1)
        row_data["Baseline CT: M(h)"] = "1" if "metastases" in ct_findings and "no metastases" not in ct_findings else "0"

    # 5. MRI Staging
    mri_match = re.search(r"MRI\s+(\d{1,2}/\d{1,2}/\d{4}):(.*?)(?:CT|MDT|\|)", table_content, re.S | re.I)
    if mri_match:
        row_data["Baseline MRI: date(h)"] = mri_match.group(1)
        mri_findings = mri_match.group(2).lower()
        t_val = re.search(r"mrT(\d[a-d]?)", mri_findings)
        n_val = re.search(r"mrN(\d[a-c]?)", mri_findings)
        if t_val: row_data["Baseline MRI: mrT(h)"] = t_val.group(1)
        if n_val: row_data["Baseline MRI: mrN(h)"] = n_val.group(1)
        if "emvi positive" in mri_findings or "emvi +" in mri_findings: row_data["Baseline MRI: mrEMVI(h)"] = "Positive"
        elif "emvi negative" in mri_findings or "emvi -" in mri_findings: row_data["Baseline MRI: mrEMVI(h)"] = "Negative"

    # 6. Entity-based fill (Chemo/Radiotherapy)
    for ent in entities:
        if ent["label"] == "CHEMO_AGENT" and not ent["negated"]:
            row_data["Chemotherapy: Drugs"] = ent["text"]
        if ent["label"] == "TREATMENT" and "radiotherapy" in ent["text"].lower() and not ent["negated"]:
            row_data["Radiotheapy: Total dose"] = "See Proforma"

    return row_data

def write_styled_workbook_vfinal(dataframe, template_path, output_path):
    workbook = load_workbook(template_path)
    worksheet = workbook.active
    template_data_row = 2
    if worksheet.max_row >= template_data_row:
        worksheet.delete_rows(template_data_row, worksheet.max_row)

    for r_idx, (_, row) in enumerate(dataframe.iterrows(), start=template_data_row):
        for c_idx, value in enumerate(row.tolist(), start=1):
            cell = worksheet.cell(row=r_idx, column=c_idx)
            val_str = ""
            if value is not None and str(value).lower() != "nan" and value != "":
                val_str = str(value)
                if val_str.endswith('.0'): val_str = val_str[:-2]
            
            if val_str == "":
                cell.value = None
            else:
                cell.value = val_str
            
            cell.number_format = '@'
            cell.data_type = 's'
    workbook.save(output_path)

def main():
    if not os.path.exists(OUTPUT_WORKBOOK.parent): os.makedirs(OUTPUT_WORKBOOK.parent)
    ner_files = sorted([f for f in os.listdir(INPUT_DIR) if f.endswith(".json")])
    all_rows = [map_ner_to_row(json.load(open(INPUT_DIR / f))) for f in ner_files]
    df = pd.DataFrame(all_rows)
    template_cols = list(pd.read_excel(PROTOTYPE_WORKBOOK).columns)
    df = df.reindex(columns=template_cols)
    write_styled_workbook_vfinal(df, PROTOTYPE_WORKBOOK, OUTPUT_WORKBOOK)
    print(f"Generated Gold Standard database saved to {OUTPUT_WORKBOOK}")

if __name__ == "__main__":
    main()
