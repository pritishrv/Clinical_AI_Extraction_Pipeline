import re


DATE_PATTERN = r"\d{1,2}[/-]\d{1,2}[/-]\d{2,4}"


def _dedupe_preserve_order(values):
    seen = set()
    result = []
    for value in values:
        cleaned = value.strip()
        if cleaned and cleaned not in seen:
            result.append(cleaned)
            seen.add(cleaned)
    return result


def _row_text(table, row_index):
    cells = []
    for cell in table.rows[row_index].cells:
        cell_text = " | ".join(
            paragraph.text.strip() for paragraph in cell.paragraphs if paragraph.text.strip()
        )
        if cell_text:
            cells.append(cell_text)
    return " | ".join(_dedupe_preserve_order(cells))


def _clean_date(value):
    if not value:
        return ""
    day, month, year = re.split(r"[/-]", value)
    if len(year) == 2:
        year = f"20{year}"
    return f"{day.zfill(2)}/{month.zfill(2)}/{year}"


def _extract_name(demo_text):
    patterns = [
        r"NHS Number:\s*\d+\s*\|+\s*Name:\s*([^|]+?)\s*\|+\s*(?:Gender|Male|Female|DOB)",
        r"NHS Number:\s*\d+\s*(?:\(c\))?\s*\|+\s*([^|]+?)\s*\|+\s*(?:Male|Female|Gender:)",
    ]
    for pattern in patterns:
        match = re.search(pattern, demo_text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return ""


def _extract_initials(name):
    cleaned = re.sub(r"^Name:\s*", "", name, flags=re.IGNORECASE).strip()
    cleaned = cleaned.replace("-", " ")
    parts = [part for part in cleaned.split() if part]
    if not parts:
        return ""
    if len(parts) == 1:
        return parts[0][0].upper()
    return f"{parts[0][0].upper()}{parts[-1][0].upper()}"


def _extract_first(pattern, text, flags=0):
    match = re.search(pattern, text, flags)
    return match.group(1).strip() if match else ""


def _extract_gender(text):
    match = re.search(r"\b(Male|Female)\b", text, re.IGNORECASE)
    return match.group(1).title() if match else ""


def _extract_previous_cancer(clinical_text):
    lowered = clinical_text.lower()
    positive_patterns = {
        "lymphoma": "lymphoma",
        "breast cancer": "breast cancer",
        "prostate cancer": "prostate cancer",
        "head and neck cancer": "head and neck cancer",
    }
    for needle, label in positive_patterns.items():
        if needle in lowered:
            return "Yes", label

    if re.search(r"\b(previous|prior|history of|known)\b.*\bcancer\b", lowered):
        snippet = _extract_first(r"\b(previous|prior|history of|known)\b[^|]{0,80}", clinical_text, re.IGNORECASE)
        return "Yes", snippet or "previous cancer"

    return "No", "N/A"


def _extract_diagnosis(diag_text, outcome_text):
    diagnosis = _extract_first(r"Diagnosis:\s*([^|]+)", diag_text, re.IGNORECASE)
    if diagnosis:
        return diagnosis

    for segment in [part.strip() for part in outcome_text.split("|") if part.strip()]:
        if re.search(r"adenocarcinoma|adenoma|dysplasia|carcinoma", segment, re.IGNORECASE):
            cleaned = re.sub(r"^(Colonoscopy|Flexi sig)\s*:\s*", "", segment, flags=re.IGNORECASE)
            return cleaned.strip()
    return ""


def _extract_histology_date(text):
    match = re.search(r"(?:biopsy|histo(?:logy)?)\s*(?:on|date)?\s*[:\-]?\s*(" + DATE_PATTERN + r")", text, re.IGNORECASE)
    return _clean_date(match.group(1)) if match else ""


def _extract_mmr(text):
    if re.search(r"\bMMR\s+deficient\b|\bdeficient\s+MMR\b", text, re.IGNORECASE):
        return "Deficient"
    if re.search(r"\bMMR\s+proficient\b|\bproficient\s+MMR\b", text, re.IGNORECASE):
        return "Proficient"
    return ""


def _extract_endoscopy(text):
    patterns = [
        r"((?:completion |repeat )?colonoscopy)\s*(?:on\s+(" + DATE_PATTERN + r"))?\s*[:\-]\s*([^|]+)",
        r"(flexi sig|sigmoidoscopy)\s*(?:on\s+(" + DATE_PATTERN + r"))?\s*[:\-]?\s*([^|]+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            raw_type, raw_date, findings = match.groups()
            endoscopy_type = "flexi sig" if "flexi" in raw_type.lower() or "sigmoidoscopy" in raw_type.lower() else "Colonoscopy complete"
            return {
                "Endoscopy: date(f)": _clean_date(raw_date),
                "Endosopy type: flexi sig, incomplete colonoscopy, colonoscopy complete - if gets to ileocecal valve(f) ": endoscopy_type,
                "Endoscopy: Findings(f)": findings.strip(),
            }
    return {
        "Endoscopy: date(f)": "",
        "Endosopy type: flexi sig, incomplete colonoscopy, colonoscopy complete - if gets to ileocecal valve(f) ": "",
        "Endoscopy: Findings(f)": "",
    }


def _extract_staging_components(text):
    result = {}

    t_match = re.search(r"(?:\b(?:mr|ct|c|p)?T)\s*([0-4](?:[a-d]|sm\d(?:/\d)?)?)", text, re.IGNORECASE)
    n_match = re.search(r"(?:\b(?:mr|ct|c|p)?N)\s*([0-3](?:[a-c])?)", text, re.IGNORECASE)
    m_match = re.search(r"(?:\b(?:mr|ct|c|p)?M)\s*([0-1](?:[a-c])?)", text, re.IGNORECASE)

    if t_match:
        result["T"] = t_match.group(1)
    if n_match:
        result["N"] = n_match.group(1)
    if m_match:
        result["M"] = m_match.group(1)

    emvi_match = re.search(r"EMVI\s*[:\-]?\s*(positive|negative|clear|unsafe|\+|-)", text, re.IGNORECASE)
    if emvi_match:
        value = emvi_match.group(1)
        result["EMVI"] = {"+" : "positive", "-" : "negative"}.get(value, value)

    crm_match = re.search(r"CRM(?:/ISP)?\s*[:\-]?\s*(clear|unsafe|threatened|involved)", text, re.IGNORECASE)
    if crm_match:
        result["CRM"] = crm_match.group(1)

    psw_match = re.search(r"PSW\s*[:\-]?\s*(clear|unsafe|\+|-)", text, re.IGNORECASE)
    if psw_match:
        value = psw_match.group(1)
        result["PSW"] = {"+" : "positive", "-" : "negative"}.get(value, value)

    return result


def _extract_modality_segment(text, modality_pattern):
    segments = [segment.strip() for segment in text.split("|") if segment.strip()]
    for segment in segments:
        if re.search(modality_pattern, segment, re.IGNORECASE):
            return segment
    return ""


def _extract_ct_fields(text, staging_text):
    ct_segment = _extract_modality_segment(text, r"\bCT\b")
    date = _extract_first(r"\bCT(?: TAP| colonography)?(?: on)?\s*(" + DATE_PATTERN + r")", ct_segment, re.IGNORECASE)
    staging_source = ct_segment or staging_text
    staging = _extract_staging_components(staging_source)

    incidental_detail = ""
    incidental_flag = ""
    incidental_match = re.search(r"incidental ([^|]+)", ct_segment, re.IGNORECASE)
    if incidental_match:
        incidental_flag = "Y"
        incidental_detail = incidental_match.group(1).strip()

    if re.search(r"no metastases|no distant metastases|no mets|no distant disease", ct_segment, re.IGNORECASE):
        m_value = "0"
    elif re.search(r"metastases|metastasis|metastatic|lung metastases|liver lesion", ct_segment, re.IGNORECASE):
        m_value = staging.get("M") or "1"
    else:
        m_value = staging.get("M", "")

    return {
        "Baseline CT: Date(h)": _clean_date(date),
        "Baseline CT: T(h)": staging.get("T", ""),
        "Baseline CT: N(h)": staging.get("N", ""),
        "Baseline CT: EMVI(h)": staging.get("EMVI", ""),
        "Baseline CT: M(h)": m_value,
        "Baseline CT: Incidental findings requiring follow up? Y/N(h)": incidental_flag,
        "Baseline CT: Detail incidental finding(h)": incidental_detail,
    }


def _extract_mri_fields(text):
    mri_segment = _extract_modality_segment(text, r"\bMR(?:I| rectum)\b")
    date = _extract_first(r"\bMR(?:I| rectum|I pelvis|I stage)?(?: [^:|]*)?(?: on)?\s*(" + DATE_PATTERN + r")", mri_segment, re.IGNORECASE)
    staging = _extract_staging_components(mri_segment)
    return {
        "Baseline MRI: date(h)": _clean_date(date),
        "Baseline MRI: mrT(h)": staging.get("T", ""),
        "Baseline MRI: mrN(h)": staging.get("N", ""),
        "Baseline MRI: mrEMVI(h)": staging.get("EMVI", ""),
        "Baseline MRI: mrCRM(h)": staging.get("CRM", ""),
        "Baseline MRI: mrPSW(h)": staging.get("PSW", ""),
    }


def _extract_treatment_approach(outcome_text):
    lowered = outcome_text.lower()
    if "foxtrot" in lowered:
        return "downstaging chemotherapy"
    if "crt" in lowered or "chemoradiotherapy" in lowered:
        return "downstaging nCRT"
    if "watch and wait" in lowered:
        return "Papillon +/- EBRT"
    if re.search(r"surgery|hemicolectomy|elape|surgical review", lowered):
        return "straight to surgery"
    return ""


def extract_case_fields_codex(case_data, doc_date=None):
    table = case_data["table"]

    demo_text = _row_text(table, 1)
    diagnosis_text = _row_text(table, 3)
    staging_text = _row_text(table, 3)
    clinical_text = _row_text(table, 5)
    outcome_text = _row_text(table, 7)
    combined_text = " | ".join([demo_text, diagnosis_text, clinical_text, outcome_text])

    name = _extract_name(demo_text)
    previous_cancer, previous_cancer_site = _extract_previous_cancer(clinical_text)
    endoscopy = _extract_endoscopy(f"{clinical_text} | {outcome_text}")
    ct_fields = _extract_ct_fields(f"{clinical_text} | {outcome_text}", staging_text)
    mri_fields = _extract_mri_fields(f"{clinical_text} | {outcome_text}")

    fields = {
        "Demographics: \nDOB(a)": _clean_date(_extract_first(r"(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\s*(?:\(a\)|Age:|Years)", demo_text, re.IGNORECASE)),
        "Demographics: Initials(b)": _extract_initials(name),
        "Demographics: MRN(c)": _extract_first(r"Hospital Number:\s*(\d+)", demo_text, re.IGNORECASE),
        "Demographics: \nNHS number(d)": _extract_first(r"NHS Number:\s*(\d+)", demo_text, re.IGNORECASE),
        "Demographics: \nGender(e)": _extract_gender(demo_text),
        "Demographics:\nPrevious cancer \n(y, n) \nif yes, where(f)": previous_cancer,
        "Demographics: \nState site of previous cancer(f)": previous_cancer_site,
        "Histology: Biopsy result(g)": _extract_diagnosis(diagnosis_text, outcome_text),
        "Histology: Biopsy date(g)": _extract_histology_date(f"{clinical_text} | {outcome_text}"),
        "Histology: \nMMR status(g/h)": _extract_mmr(combined_text),
        "1st MDT: date(i)": doc_date or "",
        "1st MDT: Treatment approach \n(TNT, downstaging chemotherapy, downstaging nCRT, downstaging shortcourse RT, Papillon +/- EBRT, straight to surgery(h)": _extract_treatment_approach(outcome_text),
        "MDT (after 6 week: Decision ": outcome_text.strip(),
    }

    fields.update(endoscopy)
    fields.update(mri_fields)
    fields.update(ct_fields)

    return fields
